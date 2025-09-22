from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("auth/", include("users.urls")),
                path("shop/", include("products.urls")),
                # Schema generation
                path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
                # Swagger UI
                path(
                    "docs/swagger/",
                    SpectacularSwaggerView.as_view(url_name="schema"),
                    name="swagger-ui",
                ),
                # Redoc UI
                path(
                    "docs/redoc/",
                    SpectacularRedocView.as_view(url_name="schema"),
                    name="redoc",
                ),
                # dj-rest-auth to avoid conflicts
                path("auth/", include("authentication.urls")),
            ]
        ),
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
