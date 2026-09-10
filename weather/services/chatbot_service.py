import datetime
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

            normalized_message = MessageParser.normalize_message(message)

            nlp_result = cls.nlp_processor.process(normalized_message)

            intent = nlp_result["intent"]
            city = nlp_result["location"]
            nlp_date = nlp_result.get("date")
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
                # try rule‑based parser first, then fallback to the previous city
                if not city:
                    # Attempt rule‑based extraction (may succeed even with high confidence)
                    rule_parsed = MessageParser.parse(normalized_message, last_city)
                    city = rule_parsed.get("city") or last_city

                parsed = {
                    "intent": intent,
                    "city": city,
                    "confidence": confidence,
                    "date": nlp_date
                }

            else:
                print("NLP confidence low -> combining NLP + rule-based parser")

                rule_parsed = MessageParser.parse(normalized_message, last_city)

                # Prefer the rule parser's intent if it found a clear one
                if rule_parsed["intent"] != "unknown":
                    final_intent = rule_parsed["intent"]
                else:
                    final_intent = intent

                # Prefer NLP's extracted city, otherwise rule parser
                final_city = city or rule_parsed.get("city") or last_city

                # Always preserve NLP date extraction
                final_date = (
                    nlp_result.get("date")
                    or rule_parsed.get("date")
                )

                parsed = {
                    "intent": final_intent,
                    "city": final_city,
                    "confidence": max(
                        confidence,
                        rule_parsed["confidence"]
                    ),
                    "date": final_date
                }

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
        # Ensure we have a city: fall back to last_city if still missing
        if not city:
            city = last_city
        confidence = parsed["confidence"]
        date_text = parsed.get("date")
        target_date = DateResolver.resolve(
        parsed.get("date")
        )

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
            if last_city:
                # Use the previously known city
                city = last_city
            else:
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
            today = datetime.date.today()
            max_forecast_date = today + datetime.timedelta(days=5)

            if target_date < today:
                return {
                    "success": False,
                    "reply": "I cannot provide historical weather. Please ask for today or upcoming days.",
                    "weather": None,
                    "last_city": last_city,
                    "intent": intent,
                }

            if target_date > max_forecast_date:
                return {
                    "success": False,
                    "reply": "I can only provide weather forecasts up to 5 days in advance.",
                    "weather": None,
                    "last_city": last_city,
                    "intent": intent,
                }

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

            date_label = target_date.strftime("%A, %d %B")

            if intent == "rain":
                reply = (
                    f"In {forecast_result['city']} on {date_label}, "
                    f"the forecast is {summary['description']} "
                    f"with a {rain_probability:.0f}% chance of rain. "
                    f"Temperatures will range from "
                    f"{summary['temperature_min']:.1f}°C to "
                    f"{summary['temperature_max']:.1f}°C."
                )

            elif intent == "humidity":
                humidity_values = [
                    entry["main"]["humidity"]
                    for entry in forecast_result["forecast"]
                ]

                min_humidity = min(humidity_values)
                max_humidity = max(humidity_values)

                reply = (
                    f"In {forecast_result['city']} on {date_label}, "
                    f"humidity is expected to range from "
                    f"{min_humidity}% to {max_humidity}%."
                )

            elif intent == "wind":
                wind_values = [
                    entry["wind"]["speed"]
                    for entry in forecast_result["forecast"]
                ]

                min_wind = min(wind_values)
                max_wind = max(wind_values)

                reply = (
                    f"In {forecast_result['city']} on {date_label}, "
                    f"wind speeds are expected to range from "
                    f"{min_wind:.1f} to {max_wind:.1f} m/s."
                )

            else:
                reply = (
                    f"In {forecast_result['city']} on {date_label}, "
                    f"expect {summary['description']} with temperatures "
                    f"between {summary['temperature_min']:.1f}°C and "
                    f"{summary['temperature_max']:.1f}°C. "
                    f"There is a {rain_probability:.0f}% chance of rain."
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