from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import CustomUser


class UserRegistrationSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = CustomUser
        fields = ["public_id", "email", "first_name", "last_name", "password"]
        read_only_fields = ["public_id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser.objects.create_user(password=password, **validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        # if not user.is_active:
        #     raise serializers.ValidationError("User account is disabled")
        data["user"] = user
        return user
