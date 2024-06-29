from enum import IntEnum, Enum


class Limits(IntEnum):
    """
    Предельные значения для моделей.
    """

    MAX_LENGTH_BRAND_TITLE = 50
    MAX_LENGTH_BRAND_DESCRIPTION = 500


class APIResponces(Enum):
    """
    Ответы API.
    """

    UNFINISHED_RENTS_EXISTS = "Существуют незавершенные аренды."
