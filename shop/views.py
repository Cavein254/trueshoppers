from django.core.cache import cache
from rest_framework import status, viewsets  # permissions
from rest_framework.response import Response

from .models import Shop
from .serializers import ShopDetailSerializer, ShopSerializer


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListAllShopsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing or retrieving shops.
    """

    def list(self, request):
        cache_key = "all_shops"
        data = cache.get(cache_key)
        if not data:
            queryset = Shop.objects.all()
            serializer = ShopSerializer(queryset, many=True)
            cache.set(cache_key, data, timeout=60 * 5)  # cache for 5 minutes

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            shop = Shop.objects.get(pk=pk)
        except shop.DoesNotExist:
            return Response(
                {"message": "Shop not found!"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ShopDetailSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)
