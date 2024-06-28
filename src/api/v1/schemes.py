from drf_spectacular.utils import OpenApiExample, OpenApiResponse

from api.v1.serializers import (
    BicycleSerializer,
    BrandGetSerializer,
    UserCreateSerializer,
)


USER_CREATE_EXAMPLE: OpenApiExample = OpenApiExample(
    name="Данные для регистрации",
    value={
        "username": "some_user",
        "email": "example@example.com",
        "password": "your-password",
    },
)

USER_CREATED_EXAMPLE: OpenApiExample = OpenApiExample(
    name="Пользователь зарегистрирован",
    value={"username": "some_user", "email": "example@example.com"},
)

USER_CREATED_201: OpenApiResponse = OpenApiResponse(
    response=UserCreateSerializer,
    description="Пользователь зарегистрирован",
    examples=[USER_CREATED_EXAMPLE],
)

BRAND_GET_EXAMPLE: OpenApiExample = OpenApiExample(
    name="Список велосипедов",
    value={
        "id": 1,
        "title": "some_title",
        "description": "Super Bike!!",
        "rental_price": "100.00",
    },
)

BICYCLE_GET_EXAMPLE: OpenApiExample = OpenApiExample(
    name="Список велосипедов",
    value={
        "id": "1",
        "brand": BRAND_GET_EXAMPLE.value,
        "available": True,
    },
)

BICYCLE_GET_200: OpenApiResponse = OpenApiResponse(
    response=BicycleSerializer,
    description="Список велосипедов",
    examples=[BICYCLE_GET_EXAMPLE],
)

BRAND_GET_200: OpenApiResponse = OpenApiResponse(
    response=BrandGetSerializer,
    description="Список марок велосипедов",
    examples=[BRAND_GET_EXAMPLE],
)
