import requests

from datetime import datetime
from django.conf import settings


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


class WeatherService:

    @staticmethod
    def get_weather(city):

        params = {
            "q": city,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric"
        }

        try:

            response = requests.get(
                BASE_URL,
                params=params,
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            return {
                "success": True,

                "city": data["name"],
                "country": data["sys"]["country"],

                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],

                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"].get("deg", 0),

                "pressure": data["main"]["pressure"],
                "visibility": data.get("visibility", 0),

                "description": data["weather"][0]["description"],
                "condition": data["weather"][0]["main"],
                "icon": data["weather"][0]["icon"]
            }

        except requests.RequestException:

            return {
                "success": False,
                "message": "Unable to fetch weather."
            }


    @staticmethod
    def get_forecast(city):

        params = {
            "q": city,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric"
        }

        try:

            response = requests.get(
                FORECAST_URL,
                params=params,
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            return {
                "success": True,
                "city": data["city"]["name"],
                "country": data["city"]["country"],
                "forecast": data["list"]
            }

        except requests.RequestException:

            return {
                "success": False,
                "message": "Unable to fetch forecast."
            }

    @staticmethod
    def get_forecast_for_date(city, target_date):
        forecast_result = WeatherService.get_forecast(city)

        if not forecast_result["success"]:
            return forecast_result

        matching_entries = []

        for entry in forecast_result["forecast"]:
            forecast_date = datetime.strptime(
                entry["dt_txt"],
                "%Y-%m-%d %H:%M:%S"
            ).date()

            if forecast_date == target_date:
                matching_entries.append(entry)

        if not matching_entries:
            return {
                "success": False,
                "message": "No forecast available for this date."
            }

        return {
            "success": True,
            "city": forecast_result["city"],
            "country": forecast_result["country"],
            "date": target_date,
            "forecast": matching_entries
        }


    @staticmethod
    def summarize_daily_forecast(forecast_entries):
        temperatures = [
            entry["main"]["temp"]
            for entry in forecast_entries
        ]

        rain_probabilities = [
            entry.get("pop", 0)
            for entry in forecast_entries
        ]

        descriptions = [
            entry["weather"][0]["description"]
            for entry in forecast_entries
        ]

        dominant_description = max(
            set(descriptions),
            key=descriptions.count
        )

        return {
            "temperature_min": min(temperatures),
            "temperature_max": max(temperatures),
            "rain_probability": max(rain_probabilities),
            "description": dominant_description,
        }