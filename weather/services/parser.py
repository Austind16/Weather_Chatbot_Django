import re
import string

class MessageParser:

    INTENTS = {
    "weather": [
        "weather",
        "temperature",
        "hot",
        "cold",
        "warm",
        "cool",
        "rain",
        "raining",
        "sunny",
        "cloudy",
    ],

    "humidity": [
        "humidity",
        "humid",
    ],

    "wind": [
        "wind",
        "windy",
        "breeze",
    ],

    "greeting": [
        "hi",
        "hello",
        "hey",
    ]
    }

    @classmethod
    def extract_standalone_city(cls, message):
    
        weather_words = {
            "weather",
            "temperature",
            "hot",
            "cold",
            "warm",
            "cool",
            "rain",
            "raining",
            "sunny",
            "cloudy",
            "humidity",
            "humid",
            "wind",
            "windy",
            "breeze",
            "forecast",
            }
    
        words = message.split()
    
        # If the message contains weather-related language,
         # don't interpret the remaining words as a city.
        if any(word in weather_words for word in words):
            return None
    
        if 1 <= len(words) <= 4:
            return message.title()
    
        return None

    @classmethod
    def parse(cls, message, last_city=None):

        message = message.lower().strip()

        intent = cls.detect_intent(message)

        city = cls.extract_city(message)

        if not city:
            city = last_city

        if intent == "unknown":
            explicit_city = cls.extract_standalone_city(message)

            if explicit_city:
                city = explicit_city
                intent = "weather"
                
        return {
            "intent": intent,
            "city": city,
            "confidence" : 1.0 if intent != "unknown" else 0.0,
            "original_message": message
        }

    @classmethod
    def detect_intent(cls, message):

        for intent, keywords in cls.INTENTS.items():

             for keyword in keywords:

                pattern = rf"\b{re.escape(keyword)}\b"

                if re.search(pattern, message):
                    return intent

        return "unknown"
    
    @classmethod
    def extract_city(cls, message):

        message = message.translate(
            str.maketrans("", "", string.punctuation)
        )

        words = message.split()

        ignored_words = {
            "weather",
            "temperature",
            "humidity",
            "humid",
            "wind",
            "windy",
            "breeze",
            "hot",
            "cold",
            "warm",
            "cool",
            "today",
            "now",
            "please",
            "in",
            "of",
            "is",
            "the",
            "what",
            "how",
            "whats",
            "tell",
            "me",
            "rain",
            "raining",
            "sunny",
            "cloudy",
            "forecast",
        }

        possible_city = [
            word
            for word in words
            if word.lower() not in ignored_words
        ]

        if not possible_city:
            return None

        return " ".join(possible_city).title()