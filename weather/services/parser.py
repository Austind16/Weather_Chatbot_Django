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
    def parse(cls, message, last_city=None):

        message = message.lower()

        intent = cls.detect_intent(message)

        city = cls.extract_city(message)

        if not city:
            city = last_city

        return {
            "intent": intent,
            "city": city,
            "confidence" : 1.0 if intent != "unknown" else 0.0,
            "original_message": message
        }

    @classmethod
    def detect_intent(cls, message):

        for intent, keywords in cls.INTENTS.items():

            if any(keyword in message for keyword in keywords):
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
            "me"
        }

        possible_city = [
            word
            for word in words
            if word.lower() not in ignored_words
        ]

        if not possible_city:
            return None

        return " ".join(possible_city).title()