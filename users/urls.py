from django.urls import path

from .views import ClientCreateView, MeView, UserLoginView, UserRegistrationView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("me/", MeView.as_view(), name="me"),
    path("tenants/", ClientCreateView.as_view(), name="tenant-create"),
]
