🎥 Real-Time Sentiment Analysis for Live Streams (YouTube + Twitch)

Overview

This project is an end-to-end Machine Learning + Backend application that performs real-time sentiment analysis on live stream chats from YouTube and Twitch.

It fetches chat messages in real time, classifies them into Positive / Negative / Neutral sentiments using NLP models, stores results in a database, and visualizes live + historical insights on an interactive dashboard.

🛠️ Tech Stack
Machine Learning (ML/NLP)

  Preprocessing: Regex cleaning, stopword removal, stemming
  
  Vectorization: TF-IDF

Models Built From Scratch:

  Logistic Regression
  
  SVM (Linear Kernel)
  
  Naive Bayes
  
  Deep Learning (ANN with Keras/TensorFlow)

Evaluation: K-Fold Cross Validation

Deployment: Saved .pkl models (model + vectorizer + encoder)

Backend

  Flask (Python)
  
  REST APIs for chat fetch + sentiment analysis
  
  PostgreSQL with SQLAlchemy ORM
  
  Flask-Migrate for schema evolution

Frontend

  HTML + Jinja Templates
  
  JavaScript (AJAX polling)
  
  Chart.js for live & historical visualizations

APIs

  YouTube Data API v3
  
  Twitch IRC (socket-based)

📂 Project Structure

/Source
│   app.py                # Flask app entrypoint
│   config.py             # Configurations
│   .env                  # API keys & DB creds
│
├── Api
│   ├── youtube_routes.py # YouTube endpoints
│   ├── twitch_routes.py  # Twitch endpoints
│   └── analyze_routes.py # Unified input (URL → platform detect)
│
├── Services
│   ├── youtube_service.py   # Fetch YouTube chats
│   ├── twitch_service.py    # Fetch Twitch chats
│   └── sentiment_service.py # Save to DB
│
├── DB
│   └── models.py         # SQLAlchemy models
│
├── ML
│   ├── model.pkl         # Trained model
│   ├── vectorizer.pkl    # TF-IDF vectorizer
│   └── encoder.pkl       # Label encoder
│
├── Utils
│   └── url_utils.py      # Extract video_id / channel
│
├── templates
│   ├── index.html        # Landing page (URL input)
│   ├── results.html      # Live sentiment chart
│   ├── history.html      # List of past streams
│   └── history_chart.html# Historical line chart

🗄️ Database Schema
Table: sentiment_results

Column	Type	Description
id	Integer (PK)	Auto-increment primary key
platform	String(20)	"youtube" or "twitch"
video_id	String(100)	YouTube video ID or Twitch channel name
timestamp	DateTime	When result was stored
positive_count	Integer	Count of positive messages
negative_count	Integer	Count of negative messages
neutral_count	Integer	Count of neutral messages

⚙️ Setup Instructions
1. Clone Repo
   git clone https://github.com/yourusername/stream-sentiment-analysis.git
  cd stream-sentiment-analysis/Source2

2. Create Virtual Environment
   python -m venv venv
  source venv/bin/activate   # Mac/Linux
  venv\Scripts\activate      # Windows

3. Install Dependencies
   pip install -r requirements.txt
   
4. Configure .env
   Create a .env file in root:
   # YouTube
  YOUTUBE_API_KEY=your_youtube_api_key

  # Twitch
  TWITCH_NICK=yourusername
  TWITCH_TOKEN=oauth:your_twitch_token
  
  # PostgreSQL
  DATABASE_URL=postgresql://username:password@localhost:5432/sentiment_db

5. Initialize Database
   flask db init
  flask db migrate -m "Initial migration"
  flask db upgrade

6. Run Flask App
   python app.py

🎯 Usage

1. Navigate to: http://127.0.0.1:5000/

2. Enter a YouTube or Twitch URL

3. See live sentiment distribution (pie chart updates every 5s)

4. Access historical sentiment trends in /history

📊 Results

  ✅ Real-time sentiment classification (Positive / Negative / Neutral)
  
  ✅ Aggregated results every 10 messages stored in DB
  
  ✅ Historical insights via line chart
  
  ✅ Model deployment-ready with .pkl files


🚧 Future Improvements

  Upgrade to Transformer models (BERT/DistilBERT) for richer semantics
  
  Support multi-language chat sentiment analysis
  
  Add moderation features (detect spam, toxicity)
  
  Containerize & deploy with Docker + AWS/GCP
  
  Add user authentication for secured dashboard access

📌 Learnings

  How traditional ML models can outperform deep learning with medium-sized datasets
  
  Importance of vectorization (TF-IDF) in short/noisy text
  
  Designing production-ready ML pipelines with Flask + SQLAlchemy
  
  Handling real-time APIs & streaming data

This project shows how to combine ML Engineering + Backend Development into a production-ready system.
  


