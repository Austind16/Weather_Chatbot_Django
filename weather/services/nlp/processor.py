import spacy
import joblib
from pathlib import Path


class NLPProcessor:

    def __init__(self):

        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")

        # Locate trained intent model
        model_path = Path(__file__).resolve().parent / "intent_model.joblib"

        # Load trained classifier
        self.intent_model = joblib.load(model_path)

    def process(self, message):

        # -------------------------
        # Intent classification
        # -------------------------

        intent = str(self.intent_model.predict([message])[0])

        # Get probability of the predicted intent
        probabilities = self.intent_model.predict_proba([message])[0]

        confidence = float(max(probabilities))

        # -------------------------
        # spaCy NLP processing
        # -------------------------

        doc = self.nlp(message)

        location = None
        date = None

        for ent in doc.ents:

            if ent.label_ in {"GPE", "LOC"} and location is None:
                location = ent.text

            elif ent.label_ in {"DATE", "TIME"} and date is None:
                date = ent.text

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