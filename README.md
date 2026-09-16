# ClimaBot

Django weather chatbot: login, chat history, hybrid intent detection (sklearn + spaCy + rules), OpenWeatherMap.

## Setup

```bash
cd Weather_Chatbot_Django
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install requests spacy scikit-learn joblib
python -m spacy download en_core_web_sm
```

Create `.env` in this folder:

```
SECRET_KEY=your-django-secret-key
DEBUG=True
OPENWEATHER_API_KEY=your-openweathermap-key
```

API key: https://openweathermap.org/api

Train the intent model (`*.joblib` is gitignored):

```bash
python weather/services/nlp/train_intent.py
```

```bash
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000 — register, then try `weather in Mumbai tomorrow`.
