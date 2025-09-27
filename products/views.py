from django.core.cache import cache
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from shop.models import Shop

from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductImageSerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def _get_user_shop(self, shop_id):
        """
        Ensure the shop belongs to the authenticated user.
        """
        try:
            return self.request.user.shops.get(id=shop_id)
        except Shop.DoesNotExist:
            raise PermissionDenied("You do not own this shop.")

    # ---------- READ WITH CACHE ----------
    def list(self, request, *args, **kwargs):
        cache_key = "all_products"
        data = cache.get(cache_key)

        if not data:  # cache miss
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=60 * 5)  # 5 minutes

        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        cache_key = f"product_{pk}"
        data = cache.get(cache_key)

        if not data:  # cache miss
            try:
                product = self.get_queryset().get(pk=pk)
            except Product.DoesNotExist:
                return Response(
                    {"message": "Product not found!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(product)
            data = serializer.data
            cache.set(cache_key, data, timeout=60 * 5)

        return Response(data, status=status.HTTP_200_OK)

    # ---------- WRITE + INVALIDATE CACHE ----------
    def perform_create(self, serializer):
        shop_id = self.request.data.get("shop_id")
        if not shop_id:
            raise PermissionDenied("A shop_id is required to create a product.")
        shop = self._get_user_shop(shop_id)
        instance = serializer.save(shop=shop)

        # invalidate caches
        cache.delete("all_products")
        cache.delete(f"product_{instance.pk}")

    def perform_update(self, serializer):
        shop_id = self.request.data.get("shop_id") or serializer.instance.shop.id
        shop = self._get_user_shop(shop_id)
        instance = serializer.save(shop=shop)

        # invalidate caches
        cache.delete("all_products")
        cache.delete(f"product_{instance.pk}")

    def perform_destroy(self, instance):
        pk = instance.pk
        super().perform_destroy(instance)

        # invalidate caches
        cache.delete("all_products")
        cache.delete(f"product_{pk}")


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def _check_user_owns_product(self, product_id):
        """
        Ensure the product belongs to a shop owned by the authenticated user.
        """
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise PermissionDenied("Product not found.")

        if product.shop not in self.request.user.shops.all():
            raise PermissionDenied("You do not own this product's shop.")

        return product

    def perform_create(self, serializer):
        product_id = self.request.data.get("product")
        if not product_id:
            raise PermissionDenied("A product_id is required to add an image.")

        product = self._check_user_owns_product(product_id)
        instance = serializer.save(product=product)

        # Invalidate product cache
        cache.delete(f"product_{product.id}")
        cache.delete("all_products")

        return instance

    def perform_update(self, serializer):
        product = serializer.instance.product
        if product.shop not in self.request.user.shops.all():
            raise PermissionDenied("You do not own this product's shop.")
        instance = serializer.save()

        # Invalidate product cache
        cache.delete(f"product_{product.id}")
        cache.delete("all_products")

        return instance

    def perform_destroy(self, instance):
        product = instance.product
        if product.shop not in self.request.user.shops.all():
            raise PermissionDenied("You do not own this product's shop.")

        super().perform_destroy(instance)

        # Invalidate product cache
        cache.delete(f"product_{product.id}")
        cache.delete("all_products")
