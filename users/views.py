from django_tenants.utils import schema_context
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Client, CustomUser
from .serializers import (
    ClientSerializer,
    CustomUserSerializer,
    UserLoginSerializer,
    UserRegistrationSerializer,
)


class MeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.public_id,
                    "email": user.email,
                    "name": f"{user.first_name} {user.last_name}",
                },
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    description="Create a new tenant",
    request=ClientSerializer,
    responses={201: ClientSerializer},
    examples=[
        OpenApiExample(
            "Tenants Creation Example",
            summary="Example of creating a shop",
            value={
                "name": "My Shop",
                "domain_url": "myshop.localhost",
                "paid_until": "2025-12-31",
                "on_trial": True,
            },
        )
    ],
)
class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        # temporarily switch to public schema

        with schema_context("public"):
            serializer.save()
