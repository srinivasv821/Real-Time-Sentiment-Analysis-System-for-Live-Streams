# this is a Logistic regression model for sentement analysis
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

#Load the data set
dataset = pd.read_csv('Tweets.csv', usecols=["airline_sentiment", "text"])
X = dataset.iloc[:, -1]
y = dataset.iloc[:, :-1]

#encode labels 
encoder = LabelEncoder()
y = encoder.fit_transform(y)


#preprocessing
# nltk.download('stopwords') # need to download only once
ps = PorterStemmer()
corpus = []

# for review in dataset['Review']:
for review in X:
    # keep only letters and replace others with space
    review = re.sub(r"@\w+", "", review) #removes all mentions "@xyz... etc"
    review = re.sub('[^a-zA-Z]', ' ',review)
    review = review.lower().split()
    # remove stopwords  + apply stemming
    review = [ps.stem(word) for word in review if word not in set(stopwords.words('english'))]
    corpus.append(" ".join(review))

# converting text --> numbers (Bag of Words)
cv = CountVectorizer(max_features=5000)
X = cv.fit_transform(corpus).toarray()

# train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 0)

# train the NB model
classifier = LogisticRegression(random_state=0, max_iter=1000)
classifier.fit(X_train, y_train)

# prediction
y_pred = classifier.predict(X_test)

# K-fold cross validation
accuracies = cross_val_score(estimator=classifier, X=X_train, y=y_train, cv=5)
print("LR Mean:", accuracies.mean(), "Std:", accuracies.std())

# Single prediction region
# review = "The abyss is out of my comprehension in the entirity of the video game."
# random_test = []
# review = re.sub('[^a-zA-Z]', ' ',review)
# review = review.lower().split()
# # remove stopwords  + apply stemming
# review = [ps.stem(word) for word in review if word not in set(stopwords.words('english'))]
# random_test.append(" ".join(review))
# print(classifier.predict(cv.transform(random_test).toarray()))

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))