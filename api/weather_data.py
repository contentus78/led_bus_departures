import requests
from datetime import datetime

def get_weather_forecast(latitude, longitude, timezone):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,precipitation_sum",
        "timezone": timezone
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def extract_today_max_temp(data):
    today = datetime.now().strftime('%Y-%m-%d')
    for i, date in enumerate(data['daily']['time']):
        if date == today:
            max_temp = data['daily']['temperature_2m_max'][i]
            max_temp_rounded = int(round(max_temp, 0))
            return f"{max_temp_rounded}°C"
    return None
