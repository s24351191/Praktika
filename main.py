import httpx
from dataclasses import dataclass

from exception import WeatherError, WeatherNetErr, WeatherParseErr

API_URL = "https://api.open-meteo.com/v1/forecast"


@dataclass
class WeatherData:
    temp: float
    hum: int
    press: int


def get_weather(lat: float, lon: float) -> WeatherData:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,pressure_msl",
        "timezone": "America/New_York",
    }

    try:
        resp = httpx.get(API_URL, params=params, timeout=30)
    except httpx.RequestError as err:
        raise WeatherNetErr(f"Ошибка сети: {err}") from err

    if resp.status_code != 200:
        raise WeatherNetErr(f"Неверный статус: {resp.status_code}")

    try:
        data = resp.json()
    except ValueError as err:
        raise WeatherParseErr(f"Не могу разобрать JSON: {err}") from err

    try:
        cur = data["current"]
        temp = cur["temperature_2m"]
        hum = cur["relative_humidity_2m"]
        press = cur["pressure_msl"]
    except KeyError as err:
        raise WeatherParseErr(f"Нет ключа в ответе: {err}") from err

    return WeatherData(temp=temp, hum=hum, press=press)


if __name__ == "__main__":
    lat = 40.7128
    lon = -74.0060
    print(f"Запрос погоды для {lat}, {lon}")

    try:
        w = get_weather(lat, lon)
        print(f"Температура: {w.temp}, Влажность: {w.hum}, Давление: {w.press}")
    except WeatherError as err:
        print(f"Что-то пошло не так: {err}")
