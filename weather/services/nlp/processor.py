import spacy
import joblib
import logging
from pathlib import Path


class NLPProcessor:

    def __init__(self):

        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")

        # Locate trained intent model
        model_path = Path(__file__).resolve().parent / "intent_model.joblib"

        # Load trained classifier – may be missing during development
        try:
            self.intent_model = joblib.load(model_path)
        except Exception as e:
            logging.info(
                "Intent model not found or failed to load (%s). "
                "Falling back to rule‑based intent detection.",
                e,
            )
            self.intent_model = None

    def process(self, message):

        # -------------------------
        # Intent classification
        # -------------------------

        if self.intent_model:
            intent = str(self.intent_model.predict([message])[0])
            probabilities = self.intent_model.predict_proba([message])[0]
            confidence = float(max(probabilities))
        else:
            # No model – treat as unknown intent with zero confidence
            intent = "unknown"
            confidence = 0.0

        # -------------------------
        # spaCy NLP processing
        # -------------------------

        # Title-case message so spaCy NER recognizes lowercase city names as GPE/LOC
        doc = self.nlp(message.title())

        location = None
        date = None

        for ent in doc.ents:

            if ent.label_ in {"GPE", "LOC"} and location is None:
                location = ent.text.lower()

            elif ent.label_ in {"DATE", "TIME"} and date is None:
                date = ent.text.lower()

        # -------------------------
        # Combined result
        # -------------------------

        return {
            "text": message,
            "tokens": [token.text for token in doc],
            "intent": intent,
            "confidence": confidence,
            "location": location,
            "date": date
        }