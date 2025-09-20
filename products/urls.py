from rest_framework_nested import routers

from .views import CategoryViewSet, ProductImageViewSet, ProductViewSet

# Base router
router = routers.DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="product")

# Nested router for product images under products
products_router = routers.NestedDefaultRouter(router, r"products", lookup="product")
products_router.register(r"images", ProductImageViewSet, basename="product-images")

urlpatterns = router.urls + products_router.urls
