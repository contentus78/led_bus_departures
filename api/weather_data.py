import requests
from datetime import datetime


def get_weather_forecast(latitude, longitude, timezone):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "daily": "temperature_2m_max,precipitation_sum",
        "timezone": timezone,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None


def extract_current_temp(data):
    current_temp = data["current_weather"]["temperature"]
    current_temp_rounded = int(round(current_temp, 0))
    return f"{current_temp_rounded}°C"


def extract_today_max_temp(data):
    today = datetime.now().strftime("%Y-%m-%d")
    for i, date in enumerate(data["daily"]["time"]):
        if date == today:
            max_temp = data["daily"]["temperature_2m_max"][i]
            max_temp_rounded = int(round(max_temp, 0))
            return f"{max_temp_rounded}°C"
    return None


if __name__ == "__main__":
    # Coordinates for bus stop Hermann-Liebmann-Str. / Eisenbahnstr.
    latitude = 51.34549642077572
    longitude = 12.405958803670908
    timezone = "Europe/Berlin"  # Example timezone

    weather_data = get_weather_forecast(latitude, longitude, timezone)
    print(weather_data)
