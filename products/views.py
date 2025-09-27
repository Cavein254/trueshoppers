from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from shop.models import Shop

from .models import Category, Product, ProductImage
from .serializers import CategorySerializer, ProductImageSerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        shop_id = self.request.data.get("shop_id")
        try:
            shop = self.request.user.shops.get(id=shop_id)
        except Shop.DoesNotExist:
            raise PermissionDenied("You do not own this shop.")
        serializer.save(shop=shop)

    def perform_update(self, serializer):
        shop_id = self.request.data.get("shop_id") or serializer.instance.shop.id
        try:
            shop = self.request.user.shops.get(id=shop_id)
        except Shop.DoesNotExist:
            raise PermissionDenied("You do not own this shop.")
        serializer.save(shop=shop)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
