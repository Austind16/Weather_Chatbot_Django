from .processor import NLPProcessor


nlp = NLPProcessor()

manual_tests = [
    # Weather
    "Can you tell me what it's like outside?",
    "Is it hot outside today?",
    "Give me the conditions in Mumbai",
    "How's the climate in Delhi?",

    # Rain
    "Should I carry an umbrella?",
    "Is there a chance I'll get wet today?",
    "Do I need rain protection?",
    "Are we expecting showers?",

    # Wind
    "How strong are the winds?",
    "Is there much air movement today?",
    "Will it be windy outside?",
    "How fast is the air moving?",

    # Humidity
    "Will it feel sticky outside?",
    "Is the air very moist today?",
    "What's the moisture level?",
    "Will it be humid tomorrow?",

    # Forecast
    "What should I expect over the next few days?",
    "What will the weather be like later this week?",
    "Show me what's coming up",
    "How are conditions expected to change?",

    # Greetings
    "Heyyy!",
    "Namaste!",
    "Good morning ClimaBot",
    "Hope you're doing well",

    # Unknown
    "What is the capital of India?",
    "Who invented the telephone?",
    "Turn on the lights",
    "What's the square root of 144?",
]

for text in manual_tests:

    result = nlp.process(text)

    print(f"Text: {text}")
    print(f"Predicted: {result['intent']}")
    print("-" * 50)