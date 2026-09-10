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

    DATE_CORRECTIONS = {
        "tommorow": "tomorrow",
        "tomorow": "tomorrow",
        "tmrw": "tomorrow",
        "todai": "today",
        "yesturday": "yesterday",
    }

    DATE_WORDS = {
        "today",
        "tomorrow",
        "yesterday",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    }

    @classmethod
    def normalize_message(cls, message):
        message = message.lower().strip()

        # Remove punctuation marks like ?, !, ., ,
        message = message.translate(str.maketrans("", "", string.punctuation))

        for wrong, correct in cls.DATE_CORRECTIONS.items():
            message = re.sub(
                rf"\b{re.escape(wrong)}\b",
                correct,
                message
            )

        return message


    @classmethod
    def extract_date(cls, message):
        for date_word in cls.DATE_WORDS:
            if re.search(rf"\b{re.escape(date_word)}\b", message):
                return date_word

        return None

    
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
    
        # Remove leading prepositions like "in ahmedabad", "at delhi", "to tokyo"
        clean_message = re.sub(r"^(in|at|for|around|to|of)\s+", "", message, flags=re.IGNORECASE).strip()
        words = clean_message.split()
    
        # If the message contains weather-related language,
        # don't interpret the remaining words as a city.
        if any(word in weather_words for word in words):
            return None
    
        if 1 <= len(words) <= 4:
            return clean_message.title()
    
        return None

    @classmethod
    def parse(cls, message, last_city=None):

        message = cls.normalize_message(message)

        intent = cls.detect_intent(message)

        city = cls.extract_city(message)

        date = cls.extract_date(message)

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
            "original_message": message,
            "date": date
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
            # Weather & condition words
            "weather",
            "temperature",
            "temp",
            "humidity",
            "humid",
            "wind",
            "windy",
            "breeze",
            "hot",
            "cold",
            "warm",
            "cool",
            "rain",
            "raining",
            "sunny",
            "cloudy",
            "forecast",

            # Time / Date words
            "today",
            "now",
            "tomorrow",
            "yesterday",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",

            # Prepositions & Articles
            "in",
            "at",
            "of",
            "to",
            "for",
            "on",
            "by",
            "the",
            "a",
            "an",

            # Question words & Verbs
            "what",
            "whats",
            "what's",
            "how",
            "ho",
            "wi",
            "tell",
            "me",
            "show",
            "give",
            "get",
            "is",
            "are",
            "was",
            "were",
            "will",
            "be",
            "being",
            "been",
            "can",
            "could",
            "would",
            "should",
            "do",
            "does",
            "did",

            # Pronouns & Fillers
            "you",
            "if",
            "it",
            "its",
            "it's",
            "there",
            "here",
            "this",
            "that",
            "like",
            "please",
            "about",
            "any",
            "some",
        }

        possible_city = [
            word
            for word in words
            if word.lower() not in ignored_words
        ]

        if not possible_city:
            return None

        return " ".join(possible_city).title()