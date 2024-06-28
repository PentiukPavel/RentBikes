from drf_spectacular.utils import OpenApiExample, OpenApiResponse

from api.v1.serializers import UserCreateSerializer


USER_CREATE_EXAMPLE = OpenApiExample(
    name="Данные для регистрации",
    value={
        "username": "some_user",
        "email": "example@example.com",
        "password": "your-password",
    },
)

USER_CREATED_EXAMPLE = OpenApiExample(
    name="Пользователь зарегистрирован",
    value={"username": "some_user", "email": "example@example.com"},
)


USER_CREATED_201: OpenApiResponse = OpenApiResponse(
    response=UserCreateSerializer,
    description="Пользователь зарегистрирован",
    examples=[USER_CREATED_EXAMPLE],
)
