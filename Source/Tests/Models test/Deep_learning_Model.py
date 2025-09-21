import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from scikeras.wrappers import KerasClassifier

# 1. Load dataset
dataset = pd.read_csv('Tweets.csv', usecols=["airline_sentiment", "text"])
X = dataset.iloc[:, -1]
y = dataset["airline_sentiment"]

#encode labels 
encoder = LabelEncoder()
y = encoder.fit_transform(y)

# 2. Preprocessing (same as before)
# nltk.download('stopwords') # need to download only once
ps = PorterStemmer()
corpus = []

for review in X:
    review = re.sub(r"@\w+", "", review) #removes all mentions "@xyz... etc"
    review = re.sub('[^a-zA-Z]', ' ', review)
    review = review.lower().split()
    review = [ps.stem(word) for word in review if word not in set(stopwords.words('english'))]
    corpus.append(" ".join(review))

# 3. Feature Extraction (TF-IDF)
tfidf = TfidfVectorizer(max_features=5000)
X = tfidf.fit_transform(corpus).toarray()

# Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# 4. Building ANN-
model = Sequential()

# Input + hidden layer 1
model.add(Dense(units=128, activation='relu', input_dim=5000))
model.add(Dropout(0.5))   # prevents overfitting

# Hidden layer 2
model.add(Dense(units=64, activation='relu'))
model.add(Dropout(0.5))

# Output layer (binary classification)
model.add(Dense(units=3, activation='softmax'))

# 5. Compile
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Adding K-fold cross validation
classifier = KerasClassifier(build_fn = model, batch_size=32, epochs=10, verbose=0)
accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=5)
print("DL Mean:", accuracies.mean(), "Std:", accuracies.std())

# 6. Train
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# 7. Evaluate
loss, acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {acc*100:.2f}%")
