import random
from io import BytesIO

import requests
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker

from shop.models import Shop

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with fake shops (with logos and cover images)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--total", type=int, default=10, help="Number of shops to create"
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = kwargs["total"]

        users = list(User.objects.all())
        if not users:
            self.stdout.write(
                self.style.ERROR(
                    "No users found. Please create at least one user first."
                )
            )
            return

        for _ in range(total):
            owner = random.choice(users)
            name = fake.unique.company()
            description = fake.text(max_nb_chars=200)

            shop = Shop(
                owner=owner,
                name=name,
                description=description,
            )

            # Download and attach fake logo
            logo_url = (
                f"https://picsum.photos/200/200?random={random.randint(1, 10000)}"
            )
            cover_url = (
                f"https://picsum.photos/800/400?random={random.randint(1, 10000)}"
            )

            try:
                logo_response = requests.get(logo_url)
                if logo_response.status_code == 200:
                    shop.logo.save(
                        f"{slugify(name)}-logo.jpg",
                        File(BytesIO(logo_response.content)),
                        save=False,
                    )

                cover_response = requests.get(cover_url)
                if cover_response.status_code == 200:
                    shop.cover_image.save(
                        f"{slugify(name)}-cover.jpg",
                        File(BytesIO(cover_response.content)),
                        save=False,
                    )
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"Image download failed: {e}"))

            shop.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {total} shops."))
