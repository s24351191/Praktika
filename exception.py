class WeatherError(Exception):
    """Ошибки с погодой."""

    pass


class WeatherNetErr(WeatherError):
    """Ошибка сети."""

    pass


class WeatherParseErr(WeatherError):
    """Ошибка парсинг."""

    pass
