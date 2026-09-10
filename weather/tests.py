import os
import sys
from pathlib import Path
import django

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from weather.services.chatbot_service import ChatbotService

print("\n==========================================")
print("TEST 1: Past Date (yesterday)")
r1 = ChatbotService.process_message("weather in mumbai yesterday")
print("Response:", r1.get("reply"))
print("Success:", r1.get("success"))

print("\n==========================================")
print("TEST 2: Beyond 5 Days (next Tuesday is 6 days away)")
r2 = ChatbotService.process_message("weather in mumbai on tuesday")
print("Response:", r2.get("reply"))
print("Success:", r2.get("success"))

print("\n==========================================")
print("TEST 3: Within 5 Days (tomorrow)")
r3 = ChatbotService.process_message("weather in mumbai tomorrow")
print("Response:", r3.get("reply"))
print("Success:", r3.get("success"))

print("\n==========================================")
print("TEST 4: Conversational Fillers ('can you tell me if it is hot in delhi')")
r4 = ChatbotService.process_message("can you tell me if it is hot in delhi")
print("Extracted City:", r4.get("last_city"))
print("Response:", r4.get("reply"))
print("Success:", r4.get("success"))

print("\n==========================================")
print("TEST 5: Standalone City with Preposition ('in ahmedabad')")
r5 = ChatbotService.process_message("in ahmedabad")
print("Extracted City:", r5.get("last_city"))
print("Response:", r5.get("reply"))
print("Success:", r5.get("success"))

print("\n==========================================")
print("TEST 6: Heavy Punctuation ('what is the humidity in mumbai?!')")
r6 = ChatbotService.process_message("what is the humidity in mumbai?!")
print("Intent:", r6.get("intent"))
print("Extracted City:", r6.get("last_city"))
print("Response:", r6.get("reply"))
print("Success:", r6.get("success"))

print("\n==========================================")
print("TEST 7: spaCy NER on Lowercase City ('weather in ahmedabad')")
r7 = ChatbotService.process_message("weather in ahmedabad")
print("Extracted City:", r7.get("last_city"))
print("Response:", r7.get("reply"))
print("Success:", r7.get("success"))
print("==========================================\n")