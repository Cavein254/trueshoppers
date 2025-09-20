# tests/test_products_api.py
import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from products.models import Category, Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_category(api_client):
    payload = {"name": "Single Origin"}
    response = api_client.post("/api/v1/shop/categories/", payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Single Origin"
    assert data["slug"] == "single-origin"


@pytest.mark.django_db
def test_create_product_with_category(api_client):
    category = Category.objects.create(name="Espresso")

    payload = {
        "name": "Dark Roast",
        "price": "1200.00",
        "stock_quantity": 20,
        "category_ids": [category.id],
    }
    response = api_client.post("/api/v1/shop/products/", payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Dark Roast"
    assert data["slug"].startswith("dark-roast")
    assert data["sku"].startswith("DAR")
    assert "espresso" in data["category"]


@pytest.mark.django_db
def test_list_products(api_client):
    Product.objects.create(name="Cold Brew", price=500, stock_quantity=3)

    response = api_client.get("/api/v1/shop/products/")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert any(p["name"] == "Cold Brew" for p in data)


@pytest.mark.django_db
def test_upload_product_image(api_client):
    product = Product.objects.create(name="Latte", price=300, stock_quantity=5)

    # Create an in-memory image
    img = Image.new("RGB", (100, 100), color="green")
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    uploaded = SimpleUploadedFile("latte.jpg", buffer.read(), content_type="image/jpeg")

    url = f"/api/v1/shop/products/{product.id}/images/"

    payload = {
        "product": product.id,  # still needed if your serializer expects it
        "image": uploaded,
        "alt_text": "Latte cup",
        "is_main": True,
    }

    response = api_client.post(
        url, payload, format="multipart"
    )  # use multipart for file upload

    assert response.status_code == 201
    data = response.json()
    assert data["alt_text"] == "Latte cup"
    assert data["thumbnail_url"] is not None
