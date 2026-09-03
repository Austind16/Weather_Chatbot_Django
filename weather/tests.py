from django.test import TestCase

# Create your tests here.
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from weather.services.weather_service import WeatherService


result = WeatherService.get_forecast("Mumbai")

print("\n--- FORECAST TEST ---")
print("Success:", result["success"])

if result["success"]:
    print("City:", result["city"])
    print("Country:", result["country"])
    print("Forecast entries:", len(result["forecast"]))

    print("\nFirst forecast entry:")
    print(result["forecast"][0])

else:
    print("Error:", result["message"])