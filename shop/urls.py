from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ListAllShopsViewSet, ShopDetailsViewSet, ShopViewSet

router = DefaultRouter()
router.register("shops", ShopViewSet, basename="shop")
router.register("shops", ListAllShopsViewSet, basename="shops")
router.register("shop-details", ShopDetailsViewSet, basename="shop-details")

urlpatterns = [
    path("", include(router.urls)),
]
