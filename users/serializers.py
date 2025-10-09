from django.contrib.auth import authenticate
from django.db import IntegrityError, transaction
from django.utils.text import slugify
from rest_framework import serializers

from .models import Client, CustomUser, Domain


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["public_id", "email", "first_name", "last_name", "date_joined"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ["public_id", "email", "first_name", "last_name", "password"]
        read_only_fields = ["public_id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")
        user = CustomUser.objects.create_user(  # type: ignore[attr-defined]
            email=email, password=password, **validated_data
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        # if not user.is_active:
        #     raise serializers.ValidationError("User account is disabled")
        attrs["user"] = user
        return attrs


class ClientSerializer(serializers.ModelSerializer):
    domain_url = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = ["name", "paid_until", "on_trial", "domain_url"]

    @transaction.atomic
    def create(self, validated_data):
        domain_url = validated_data.pop("domain_url").strip().lower()

        schema_name = slugify(validated_data["name"]).replace("-", "_")

        if not schema_name.isidentifier():
            raise serializers.ValidationError(
                {"schema_name": "Invalid schema name. Use letters, digits"}
            )

        if Client.objects.filter(schema_name=schema_name).exists():
            raise serializers.ValidationError(
                {"domain_url": "A domain with a similar name already exists"}
            )
        try:
            client = Client.objects.create(schema_name=domain_url, **validated_data)

            Domain.objects.create(domain=domain_url, tenant=client, is_primary=True)
        except IntegrityError as e:
            raise serializers.ValidationError(
                {"schema_name": f"Database constraint violated: {str(e)}"}
            )

        return client
