import os
from joblib import load

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = load(os.path.join(BASE_DIR, "sentiment_model.pkl"))
vectorizer = load(os.path.join(BASE_DIR, "sentiment_model_vectorizer.pkl"))
encoder = load(os.path.join(BASE_DIR, "sentiment_model_encoder.pkl"))
