import random
import uuid

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from faker import Faker

from products.models import Category, Product, ProductImage
from shop.models import Shop

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with products and random images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=20,
            help="Number of products to create per shop",
        )

    def handle(self, *args, **options):
        count = options["count"]

        shops = Shop.objects.all()
        if not shops.exists():
            self.stdout.write(self.style.ERROR("⚠️ No shops found. Create shops first."))
            return

        categories = list(Category.objects.all())
        if not categories:
            # create fallback categories
            categories = [
                Category.objects.create(name="Electronics"),
                Category.objects.create(name="Clothing"),
                Category.objects.create(name="Books"),
                Category.objects.create(name="Furniture"),
                Category.objects.create(name="Footwear"),
                Category.objects.create(name="Textile"),
                Category.objects.create(name="Fast Food"),
            ]

        for shop in shops:
            self.stdout.write(
                self.style.NOTICE(f"📦 Seeding {count} products for shop: {shop.name}")
            )

            for _ in range(count):
                product = Product.objects.create(
                    shop=shop,
                    name=fake.sentence(nb_words=3),
                    description=fake.paragraph(nb_sentences=3),
                    price=round(random.uniform(10, 500), 2),
                    stock_quantity=random.randint(1, 100),
                )

                # attach random categories
                product.category.set(random.sample(categories, k=random.randint(1, 2)))

                # Generate 2–5 random images
                num_images = random.randint(2, 5)
                for i in range(num_images):
                    image_url = (
                        f"https://picsum.photos/600/600?random={uuid.uuid4().hex}"
                    )
                    resp = requests.get(image_url)
                    if resp.status_code == 200:
                        image_name = f"product_{product.id}_{i}.webp"
                        image_file = ContentFile(resp.content, name=image_name)
                        ProductImage.objects.create(
                            product=product,
                            image=image_file,
                            alt_text=fake.sentence(nb_words=4),
                            is_main=(i == 0),  # first image is main
                        )

                self.stdout.write(
                    self.style.SUCCESS(f"✅ Created product: {product.name}")
                )

        self.stdout.write(self.style.SUCCESS("🎉 Done seeding products!"))
