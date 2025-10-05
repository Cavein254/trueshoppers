import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from users.models import CustomUser


class Command(BaseCommand):
    help = "Seed the database with test users and a superuser"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding users..."))

        # Create superuser if not exists
        if not CustomUser.objects.filter(email="admin@example.com").exists():
            CustomUser.objects.create_superuser(
                email="admin@example.com",
                password="admin123",
                first_name="Admin",
                last_name="User",
            )
            self.stdout.write(
                self.style.SUCCESS("✅ Created superuser: admin@example.com / admin123")
            )
        else:
            self.stdout.write("⚠️ Superuser already exists.")

        # Create normal users
        first_names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller"]

        for i in range(10):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}{i}@example.com"
            password = "password123"

            if not CustomUser.objects.filter(email=email).exists():
                CustomUser.objects.create_user(
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    date_joined=timezone.now(),
                )
                self.stdout.write(self.style.SUCCESS(f"✅ Created user: {email}"))
            else:
                self.stdout.write(f"⚠️ User already exists: {email}")

        self.stdout.write(self.style.SUCCESS("🎉 Done seeding users!"))
