from django.contrib.auth import get_user_model
from factory import (
    Faker,
    PostGenerationMethodCall,
    Sequence,
)
from factory.django import DjangoModelFactory

User = get_user_model()

PASSWORD = "example"


class UserFactory(DjangoModelFactory):
    """Фабрика для создания экземпляров модели Пользователь."""

    class Meta:
        model = User

    username = Sequence(lambda n: "user_{}".format(n))
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    email = Sequence(lambda n: "{}@example.org".format(n))
    is_superuser = False
    is_active = True
    password = PostGenerationMethodCall("set_password", PASSWORD)
