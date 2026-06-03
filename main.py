import httpx

API_URL = "https://api.open-meteo.com/v1/forecast"


def get_weather(latitude: float, longitude: float):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,pressure_msl",
        "timezone": "Europe/Moscow",
    }

    try:
        response = httpx.get(API_URL, params=params)
        response.raise_for_status()
        weather_data = response.json()
        current_weather = weather_data.get("current", {})
        temperature = current_weather.get("temperature_2m")
        humidity = current_weather.get("relative_humidity_2m")
        pressure = current_weather.get("pressure_msl")
        return temperature, humidity, pressure
    except httpx.RequestError as e:
        print(f"Ошибка при запросе к API: {e}")
        return None, None, None
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")
        return None, None, None


if __name__ == "__main__":
    lat = 55.7558
    lon = 37.6173
    print(f"Запрашиваем погоду для координат: широта {lat}, долгота {lon}")
    temp, hum, press = get_weather(lat, lon)
    if temp is not None:
        print("\n--- Результат ---")
        print(f"Температура: {temp}°C")
        print(f"Относительная влажность: {hum}%")
        print(f"Давление: {press} гПа")
    else:
        print("\nНе удалось получить данные о погоде.")
