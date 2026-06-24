from enum import StrEnum, auto


class WeatherRequestErrorKind(StrEnum):
    """Тип ошибки которая произошла при запросе погоды."""

    NET = auto()
    """Сетевая ошибка."""
    PARSE = auto()
    """Ошибка парсинга данных."""


class WeatherRequestError(Exception):
    """Ошибка запроса погоды."""

    def __init__(self, description: str, kind: WeatherRequestErrorKind) -> None:
        self.description = description
        self.kind = kind
        super().__init__(f"{kind.name}: {description}")
