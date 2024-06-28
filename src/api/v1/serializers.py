from rest_framework import serializers

from django.contrib.auth import get_user_model

from bicycles.models import Bicycle, Brand

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя."""

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")


class BrandGetSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации о марке велосипеда."""

    class Meta:
        model = Brand
        fields = ("id", "title", "description", "rental_price")


class BicycleSerializer(serializers.ModelSerializer):
    """Сериализатор для получения информации велосипеде."""

    brand = BrandGetSerializer()

    class Meta:
        model = Bicycle
        fields = ("id", "brand", "available")
