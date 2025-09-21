# this is a SVM model for sentement analysis
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# nltk.download('stopwords') # need to download only once


# Load dataset
df = pd.read_csv('Tweets.csv', usecols=['airline_sentiment', 'text'])
df.dropna(subset=['airline_sentiment', 'text'], inplace=True)
df = df.reset_index(drop=True)

# Label encoding
le = LabelEncoder()
y = le.fit_transform(df['airline_sentiment']) 

# Preprocessing function
ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text: str) -> str:
    text = str(text)
    # remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # remove mentions and RT token
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'\brt\b', '', text, flags=re.I)
    # remove non-letters
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    # tokenize, lowercase, remove stopwords, stem
    tokens = text.lower().split()
    tokens = [ps.stem(t) for t in tokens if t not in stop_words and len(t) > 1]
    return ' '.join(tokens)

# Apply preprocessing
print("Preprocessing texts...")
corpus = df['text'].apply(preprocess_text)


# Vectorize with TF-IDF
tfidf = TfidfVectorizer(max_features=5000) 
X = tfidf.fit_transform(corpus)              

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0, stratify=y
)


# Train SVM (linear kernel).
print("Training SVM (this can take a while on big data)...")
classifier = SVC(kernel='linear', random_state=0)
classifier.fit(X_train, y_train)


# Cross-validation on training set
print("Running cross-validation (5-fold) on training data...")
cv_scores = cross_val_score(
    SVC(kernel='linear', random_state=0),
    X_train, y_train, cv=5, n_jobs=-1, scoring='accuracy'
)
print(f"CV accuracy mean: {cv_scores.mean():.4f}, std: {cv_scores.std():.4f}")

# Evaluate on test set
y_pred = classifier.predict(X_test)
print("\nTest set results:")
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification report:")
print(classification_report(y_test, y_pred, target_names=le.classes_))
print("\nConfusion matrix:")
print(confusion_matrix(y_test, y_pred))


# Save artifacts for later use 

# joblib.dump(classifier, "svm_tweet_sentiment_model.pkl")
# joblib.dump(tfidf, "tfidf_vectorizer.pkl")
# joblib.dump(le, "label_encoder.pkl")
# print("\nSaved model -> svm_tweet_sentiment_model.pkl")
# print("Saved vectorizer -> tfidf_vectorizer.pkl")
# print("Saved label encoder -> label_encoder.pkl")


# Quick predict function example

def predict_text(text: str) -> str:
    cleaned = preprocess_text(text)
    vec = tfidf.transform([cleaned])
    pred = classifier.predict(vec)[0]
    return le.inverse_transform([pred])[0]

# Example
example = "I loved the flight, the crew was amazing and service was great!"
print("\nExample prediction:", example, "->", predict_text(example))
