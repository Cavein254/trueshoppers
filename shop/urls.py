from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ListAllShopsViewSet, MyShopsViewSet, ShopDetailsViewSet, ShopViewSet

router = DefaultRouter()
router.register("shops", ShopViewSet, basename="shop")
router.register("shops", ListAllShopsViewSet, basename="shops")
router.register("shop-details", ShopDetailsViewSet, basename="shop-details")
router.register("myshops", MyShopsViewSet, basename="myshops")

urlpatterns = [
    path("", include(router.urls)),
]
