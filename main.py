import httpx
from dataclasses import dataclass
from exception import WeatherRequestError, WeatherRequestErrorKind

API_URL = "https://api.open-meteo.com/v1/forecast"


@dataclass
class WeatherData:
    temperature: float
    humidity: int
    pressure: int


def get_weather(latitude: float, longitude: float) -> WeatherData:
    params: dict[str, float | str] = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,pressure_msl",
        "timezone": "Europe/Moscow",
    }

    try:
        resp = httpx.get(API_URL, params=params, timeout=30)
    except httpx.RequestError as err:
        raise WeatherRequestError(
            f"Ошибка сети: {err}", WeatherRequestErrorKind.NET
        ) from err

    if resp.status_code != 200:
        raise WeatherRequestError(
            f"Неверный статус: {resp.status_code}", WeatherRequestErrorKind.NET
        )

    try:
        data = resp.json()
    except ValueError as err:
        raise WeatherRequestError(
            f"Не могу разобрать JSON: {err}", WeatherRequestErrorKind.PARSE
        ) from err

    try:
        current = data["current"]
        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        pressure = current["pressure_msl"]
    except KeyError as err:
        raise WeatherRequestError(
            f"Нет ключа в ответе: {err}", WeatherRequestErrorKind.PARSE
        ) from err

    return WeatherData(
        temperature=temperature, humidity=humidity, pressure=pressure
    )


if __name__ == "__main__":
    latitude = 55.7558
    longitude = 37.6173

    print(f"Запрос погоды для {latitude}, {longitude}")

    try:
        weth = get_weather(latitude, longitude)
        print(
            f"Температура: {weth.temperature}, "
            f"Влажность: {weth.humidity}, "
            f"Давление: {weth.pressure}"
        )
    except WeatherRequestError as err:
        print(f"Что-то пошло не так: {err}")
