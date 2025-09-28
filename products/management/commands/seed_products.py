import random
import uuid

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from faker import Faker

from products.models import Category, Product, ProductImage
from shop.models import Shop


class Command(BaseCommand):
    help = "Seed the database with fake products and categories"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total",
            type=int,
            default=20,
            help="Number of products to create",
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs["total"]

        shops = list(Shop.objects.all())
        if not shops:
            self.stdout.write(
                self.style.ERROR("No shops found. Please seed shops first.")
            )
            return

        # Create some categories if none exist
        if Category.objects.count() == 0:
            for _ in range(5):
                Category.objects.create(name=fake.word().capitalize())
            self.stdout.write(self.style.SUCCESS("Created some sample categories."))

        categories = list(Category.objects.all())

        for _ in range(total):
            shop = random.choice(shops)
            category = random.sample(categories, k=random.randint(1, 2))

            product = Product.objects.create(
                shop=shop,
                name=fake.catch_phrase(),
                description=fake.paragraph(nb_sentences=3),
                price=round(random.uniform(5.0, 500.0), 2),
                stock_quantity=random.randint(0, 100),
            )
            product.category.set(category)

            # Add 1–5 product images
            for i in range(random.randint(1, 5)):
                try:
                    response = requests.get("https://picsum.photos/600", timeout=10)
                    if response.status_code == 200:
                        img_name = f"{uuid.uuid4()}.jpg"
                        ProductImage.objects.create(
                            product=product,
                            alt_text=fake.word(),
                            is_main=(i == 0),
                            image=ContentFile(response.content, img_name),
                        )
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Image fetch failed: {e}"))

            self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully created {total} products!"))
