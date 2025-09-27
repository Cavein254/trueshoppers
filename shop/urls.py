from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ListAllShopsViewSet, ShopViewSet

router = DefaultRouter()
router.register("shops", ShopViewSet, basename="shop")
router.register("shops", ListAllShopsViewSet, basename="shops")

urlpatterns = [
    path("", include(router.urls)),
]
