import requests

from django.conf import settings


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


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