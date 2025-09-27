from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Category, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "alt_text", "is_main", "thumbnail_url"]

    @extend_schema_field(serializers.CharField(allow_null=True))
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            return obj.thumbnail.url
        return None


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "children", "products"]
        read_only_fields = ["slug"]

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), many=True).data

    @extend_schema_field(serializers.ListField(child=serializers.DictField()))
    def get_products(self, obj):
        products = Product.objects.filter(category=obj)
        return ProductSerializer(products, many=True).data


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="slug"
    )
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), write_only=True, source="category"
    )
    shop_id = serializers.IntegerField(write_only=True)
    shop = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "shop",
            "shop_id",
            "name",
            "slug",
            "sku",
            "price",
            "stock_quantity",
            "images",
            "description",
            "category",
            "category_ids",
        ]
        read_only_fields = ["slug", "sku"]
