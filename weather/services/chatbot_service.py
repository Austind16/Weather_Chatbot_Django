from datetime import date
from .parser import MessageParser
from .weather_service import WeatherService
from .nlp.processor import NLPProcessor
from .date_resolver import DateResolver


class ChatbotService:

    # Create NLP processor once
    nlp_processor = NLPProcessor()

    @classmethod
    def process_message(cls, message, last_city=None):

        # --------------------------------
        # 1. Try NLP first
        # --------------------------------

        try:

            nlp_result = cls.nlp_processor.process(message)

            intent = nlp_result["intent"]
            city = nlp_result["location"]
            confidence = nlp_result["confidence"]

            print("\n--- NLP RESULT ---")
            print(nlp_result)

            # --------------------------------
            # 2. Check NLP confidence
            # --------------------------------

            if confidence >= 0.50:

                print("Using NLP result")

                # If NLP didn't find a city,
                # use the previous city if available
                if not city:
                    city = last_city

                parsed = {
                    "intent": intent,
                    "city": city,
                    "confidence": confidence,
                    "date": nlp_result["date"]
                }

            else:

                print("NLP confidence too low → using rule-based parser")

                parsed = MessageParser.parse(
                    message,
                    last_city
                )
                parsed["date"] = None

        except Exception as e:

            print("\nNLP ERROR:", e)
            print("Falling back to rule-based parser")

            parsed = MessageParser.parse(
                message,
                last_city
            )

        # --------------------------------
        # 3. Get parsed information
        # --------------------------------

        intent = parsed["intent"]
        city = parsed["city"]
        confidence = parsed["confidence"]
        date_text = parsed.get("date")
        target_date = DateResolver.resolve(date_text)

        # --------------------------------
        # 4. Greeting
        # --------------------------------

        if intent == "greeting":

            return {
                "success": True,
                "reply": "Hello! 👋 Ask me about the weather.",
                "weather": None,
                "last_city": last_city,
                "intent": intent,
            }

        # --------------------------------
        # 5. Low confidence
        # --------------------------------

        if confidence < 0.5:

            return {
                "success": False,
                "reply": "I'm not sure what you mean. Could you rephrase that?",
                "weather": None,
                "last_city": last_city,
                "intent": intent,
            }

        # --------------------------------
        # 6. No city available
        # --------------------------------

        if not city:

            return {
                "success": False,
                "reply": "Please tell me which city you're asking about.",
                "weather": None,
                "last_city": last_city,
                "intent": intent,
            }

        # --------------------------------
        # 7. Get weather
        # --------------------------------

        if target_date:
            forecast_result = WeatherService.get_forecast_for_date(
                city,
                target_date
            )

            if not forecast_result["success"]:
                return {
                    "success": False,
                    "reply": forecast_result["message"],
                    "weather": None,
                    "last_city": last_city,
                    "intent": intent,
                }

            summary = WeatherService.summarize_daily_forecast(
                forecast_result["forecast"]
            )

            rain_probability = summary["rain_probability"] * 100

            if intent == "rain":
                reply = (
                    f"In {forecast_result['city']} tomorrow, "
                    f"the forecast is {summary['description']} "
                    f"with a {rain_probability:.0f}% chance of rain. "
                    f"Temperatures will range from "
                    f"{summary['temperature_min']:.1f}°C to "
                    f"{summary['temperature_max']:.1f}°C."
                )

            else:
                reply = (
                    f"In {forecast_result['city']} tomorrow, "
                    f"expect {summary['description']} with temperatures "
                    f"between {summary['temperature_min']:.1f}°C and "
                    f"{summary['temperature_max']:.1f}°C."
                )

            return {
                "success": True,
                "reply": reply,
                "weather": forecast_result,
                "last_city": forecast_result["city"],
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

        # --------------------------------
        # 8. Generate response
        # --------------------------------

        replies = {

            "weather":
                f"In {weather['city']}, it's "
                f"{weather['temperature']}°C with "
                f"{weather['description']}.",

            "humidity":
                f"Humidity in {weather['city']} "
                f"is {weather['humidity']}%.",

            "wind":
                f"Wind speed in {weather['city']} "
                f"is {weather['wind_speed']} m/s.",

            "rain":
                f"In {weather['city']}, the current "
                f"condition is {weather['description']}.",

        }

        return {
            "success": True,
            "reply": replies.get(
                intent,
                "Sorry, I couldn't understand that."
            ),
            "weather": weather,
            "last_city": weather["city"],
            "intent": intent,
        }