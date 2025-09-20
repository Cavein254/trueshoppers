from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, ProductImageViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"all", ProductViewSet, basename="all-products")
router.register(r"product-images", ProductImageViewSet, basename="productimage")

urlpatterns = router.urls
