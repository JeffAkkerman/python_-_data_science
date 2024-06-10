"""
A script that calls on an API to get the weather forecast
of selected cities and returns the high and low temp with
an emoji to show if it is sunny, cloudly, raining, etc.

Open-metro.com API Documentation: https://open-meteo.com/en/docs
"""

import requests
import requests_cache
import pandas as pd
from retrying import retry

# Setup cache and retry
requests_cache.install_cache('weather_cache', expire_after=3600)


@retry(stop_max_attempt_number=5, wait_fixed=200)
def fetch_weather_data(url, params):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


# List of coordinates for selected cities
cities = [
    {"name": "Abilene", "latitude": 32.4487, "longitude": -99.7331},
    {"name": "Amarillo", "latitude": 35.222, "longitude": -101.8313},
    {"name": "Austin", "latitude": 30.2672, "longitude": -97.7431},
    {"name": "Brownsville", "latitude": 25.9017, "longitude": -97.4975},
    {"name": "Corpus Christi", "latitude": 27.8006, "longitude": -97.3964},
    {"name": "DFW", "latitude": 32.8998, "longitude": -97.0403},
    {"name": "El Paso", "latitude": 31.7619, "longitude": -106.4850},
    {"name": "Houston", "latitude": 29.7604, "longitude": -95.3698},
    {"name": "Lubbock", "latitude": 33.5779, "longitude": -101.8552},
    {"name": "San Antonio", "latitude": 29.4241, "longitude": -98.4936},
    {"name": "Texarkana", "latitude": 33.4418, "longitude": -94.0377}
]

# API URL and parameters
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "daily": ["weathercode", "temperature_2m_max", "temperature_2m_min"],
    "temperature_unit": "fahrenheit",
    "wind_speed_unit": "mph",
    "precipitation_unit": "inch",
    "forecast_days": 1,
    "timezone": "auto"
}


# Function to map weather codes to emojis
def get_weather_emoji(weather_code):
    emoji = ""
    if weather_code == 0:
        emoji = "☀️"
    elif weather_code == 1:
        emoji = "🌤️"
    elif weather_code == 2:
        emoji = "⛅"
    elif weather_code == 3:
        emoji = "☁️"
    elif weather_code in [45, 48]:
        emoji = "🌫️"
    elif weather_code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
        emoji = "🌧️"
    elif weather_code in [71, 73, 75, 77, 85, 86]:
        emoji = "❄️"
    elif weather_code in [95, 96, 99]:
        emoji = "⛈️"
    return emoji


# Fetch and process weather data for each city
weather_info = ""
for city in cities:
    city_params = params.copy()
    city_params["latitude"] = city["latitude"]
    city_params["longitude"] = city["longitude"]

    data = fetch_weather_data(url, city_params)
    daily_data = data['daily']

    df = pd.DataFrame({
        "date": daily_data['time'],
        "weather_code": daily_data['weathercode'],
        "temperature_2m_max": daily_data['temperature_2m_max'],
        "temperature_2m_min": daily_data['temperature_2m_min']
    })

    weather_code = df.loc[0, 'weather_code']
    high_temp = df.loc[0, 'temperature_2m_max']
    low_temp = df.loc[0, 'temperature_2m_min']
    emoji = get_weather_emoji(weather_code)

    weather_info += f"{city['name']} {emoji} {high_temp}/{low_temp}° | "

# Remove the trailing separator and wrap in HTML tags
weather_info = weather_info.rstrip(" | ")
html_output = f"<p>{weather_info}</p>"

print(html_output)
