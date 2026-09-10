import json
from django.test import TestCase, Client
from django.urls import reverse

class ChatbotServiceTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Initialize fresh session data
        session = self.client.session
        session['conversation'] = []
        session['last_city'] = None
        session.save()

    def test_greeting_intent(self):
        """A simple greeting should be recognized and responded to without asking for a city."""
        response = self.client.post(
            reverse('chat_api'),
            data=json.dumps({"message": "hello"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('response', data)
        self.assertNotIn('ask_city', data)
        self.assertTrue(any(g in data['response'].lower() for g in ['hello', 'hi', 'hey']))

    def test_weather_without_city_uses_last_city(self):
        """When a user asks for weather but omits the city, the service should fall back to the last known city."""
        # First interaction to set a last_city
        self.client.post(
            reverse('chat_api'),
            data=json.dumps({"message": "weather in mumbai tomorrow"}),
            content_type='application/json'
        )
        # Second interaction without city
        response = self.client.post(
            reverse('chat_api'),
            data=json.dumps({"message": "what's the weather tomorrow"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('response', data)
        self.assertIn('mumbai', data['response'].lower())

    def test_unknown_intent_prompts_city(self):
        """When the intent is unknown and no city is known, the bot should ask for a city."""
        response = self.client.post(
            reverse('chat_api'),
            data=json.dumps({"message": "recommend a restaurant"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('ask_city', data)
        self.assertTrue(data['ask_city'])

    def test_clear_chat_resets_session(self):
        """Calling the clear‑chat endpoint should reset the conversation and last_city."""
        # Populate session
        session = self.client.session
        session['conversation'] = [{'role': 'user', 'content': 'hi'}]
        session['last_city'] = 'delhi'
        session.save()
        # Hit clear endpoint
        response = self.client.get(reverse('clear_chat'))
        self.assertEqual(response.status_code, 200)
        # Verify session cleared
        self.assertEqual(self.client.session.get('conversation'), [])
        self.assertIsNone(self.client.session.get('last_city'))
