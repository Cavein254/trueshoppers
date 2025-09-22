# tests/test_products.py
import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.text import slugify
from PIL import Image

from products.models import Category, Product, ProductImage
from products.serializers import (
    CategorySerializer,
    ProductImageSerializer,
    ProductSerializer,
)


@pytest.mark.django_db
def test_category_slug_autogeneration():
    cat = Category.objects.create(name="Coffee Beans")
    assert cat.slug == slugify("Coffee Beans")


@pytest.mark.django_db
def test_product_slug_and_sku_autogeneration():
    product = Product.objects.create(
        name="Kenya AA Coffee",
        price=1200.50,
        stock_quantity=10,
    )
    assert product.slug.startswith("kenya-aa-coffee")
    assert product.sku.startswith("KEN")


@pytest.mark.django_db
def test_product_slug_uniqueness():
    p1 = Product.objects.create(name="Espresso Blend", price=500, stock_quantity=5)
    p2 = Product.objects.create(name="Espresso Blend", price=600, stock_quantity=8)

    assert p1.slug == "espresso-blend"
    assert p2.slug.startswith("espresso-blend-")  # incremented slug


@pytest.mark.django_db
def test_product_category_relationship():
    cat = Category.objects.create(name="Filter Coffee")
    product = Product.objects.create(name="V60 Brew", price=300, stock_quantity=4)
    product.category.add(cat)

    assert product in cat.products.all()
    assert cat in product.category.all()


@pytest.mark.django_db
def test_product_image_webp_conversion(tmp_path):
    # Create a fake image
    img = Image.new("RGB", (100, 100), color="red")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    uploaded = SimpleUploadedFile("test.jpg", buffer.read(), content_type="image/jpeg")

    product = Product.objects.create(name="Drip Coffee", price=200, stock_quantity=2)
    product_image = ProductImage.objects.create(product=product, image=uploaded)

    assert product_image.image.name.endswith(".webp")


# ---- SERIALIZER TESTS ----


@pytest.mark.django_db
def test_product_serializer_output():
    cat = Category.objects.create(name="Specialty")
    product = Product.objects.create(name="Cold Brew", price=800, stock_quantity=7)
    product.category.add(cat)

    serializer = ProductSerializer(product)
    data = serializer.data

    assert data["name"] == "Cold Brew"
    assert data["slug"].startswith("cold-brew")
    assert data["sku"].startswith("COL")
    assert "specialty" in data["category"]


@pytest.mark.django_db
def test_category_serializer_with_children_and_products():
    parent = Category.objects.create(name="Coffee")
    child = Category.objects.create(name="Arabica", parent=parent)
    product = Product.objects.create(name="AA Plus", price=1500, stock_quantity=5)
    product.category.add(child)

    serializer = CategorySerializer(parent)
    data = serializer.data

    assert any(c["name"] == "Arabica" for c in data["children"])
    assert not data["products"]  # parent itself has no direct products

    serializer_child = CategorySerializer(child)
    data_child = serializer_child.data
    assert any(p["name"] == "AA Plus" for p in data_child["products"])


@pytest.mark.django_db
def test_product_image_serializer_thumbnail(tmp_path):
    img = Image.new("RGB", (100, 100), color="blue")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    uploaded = SimpleUploadedFile("thumb.jpg", buffer.read(), content_type="image/jpeg")
    product = Product.objects.create(name="Latte", price=350, stock_quantity=5)
    product_image = ProductImage.objects.create(product=product, image=uploaded)

    serializer = ProductImageSerializer(product_image)
    data = serializer.data

    assert data["thumbnail_url"] is not None
    assert data["alt_text"] == ""
