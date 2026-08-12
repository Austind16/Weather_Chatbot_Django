from .parser import MessageParser
from .weather_service import WeatherService


class ChatbotService:

    @classmethod
    def process_message(cls, message, last_city=None):

        parsed = MessageParser.parse(message, last_city)

        intent = parsed["intent"]
        city = parsed["city"]
        confidence = parsed["confidence"]

        # Greeting
        if intent == "greeting":
            return {
                "success": True,
                "reply": "Hello! 👋 Ask me about the weather.",
                "weather": None,
                "last_city": last_city,
                "intent": intent,
            }

        # Low confidence
        if confidence < 0.5:
            return {
                "success": False,
                "reply": "I'm not sure what you mean. Could you rephrase that?",
                "weather": None,
                "last_city": last_city,
                "intent": intent,
            }

        # No city available
        if not city:
            return {
                "success": False,
                "reply": "Please tell me which city you're asking about.",
                "weather": None,
                "last_city": last_city,
                "intent": intent,
            }

        weather = WeatherService.get_weather(city)

        if not weather["success"]:
            return {
                "success": False,
                "reply": weather["message"],
                "weather": None,
                "last_city": last_city,
                "intent": intent,
            }

        replies = {
            "weather":
                f"In {weather['city']}, it's {weather['temperature']}°C with {weather['description']}.",

            "humidity":
                f"Humidity in {weather['city']} is {weather['humidity']}%.",

            "wind":
                f"Wind speed in {weather['city']} is {weather['wind_speed']} m/s."
        }

        return {
            "success": True,
            "reply": replies.get(intent, "Sorry, I couldn't understand that."),
            "weather": weather,
            "last_city": weather["city"],
            "intent": intent,
        }