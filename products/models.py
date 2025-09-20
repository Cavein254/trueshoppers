import uuid
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=False)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )
    stock_quantity = models.PositiveBigIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug
        if not self.sku:
            base = self.name[:3].upper()
            unique = str(uuid.uuid4().int)[:6]
            self.sku = f"{base}-{unique}"

    def __str__(self):
        return f"{self.product.name} -  {self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        "Product", related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to="products/"
    )  # store only one file (WebP recommended)
    alt_text = models.CharField(max_length=255, blank=True)
    is_main = models.BooleanField(default=False)

    # Dynamic thumbnail (200x200 WebP) generated on the fly
    thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(200, 200)],
        format="WEBP",
        options={"quality": 75},
    )

    def save(self, *args, **kwargs):
        # Optional: convert uploaded image to WebP before saving
        if self.image:
            img = Image.open(self.image)
            img = img.convert("RGB")
            buffer = BytesIO()
            img.save(buffer, format="WEBP", quality=85)
            self.image.save(
                self.image.name.split(".")[0] + ".webp",
                ContentFile(buffer.getvalue()),
                save=False,
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.product.name}"
