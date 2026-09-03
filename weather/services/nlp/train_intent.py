from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from .intent_data import TRAINING_DATA
import joblib


# Separate text and labels
texts = [text for text, intent in TRAINING_DATA]
labels = [intent for text, intent in TRAINING_DATA]


# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)


# Create NLP pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# Train
model.fit(X_train, y_train)

joblib.dump(
    model,
    "weather/services/nlp/intent_model.joblib"
)

print("Intent model saved successfully.")

# Evaluate
predictions = model.predict(X_test)

y_pred = model.predict(X_test)

for text, actual, predicted in zip(X_test, y_test, y_pred):
    if actual != predicted:
        print(
            f"\nText: {text}"
            f"\nActual: {actual}"
            f"\nPredicted: {predicted}"
        )

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=model.classes_
)

print("\nConfusion Matrix:\n")
print(cm)

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=model.classes_
)

disp.plot(xticks_rotation=45)

plt.tight_layout()
plt.show()