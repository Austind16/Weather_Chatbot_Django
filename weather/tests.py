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
print("==========================================\n")