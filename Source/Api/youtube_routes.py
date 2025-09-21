from flask import jsonify, Blueprint, render_template
from Services.youtube_service import fetch_youtube_chat
from ML.Load_model import model, vectorizer, encoder  # load your saved pkl files
from Services.sentiment_service import store_sentiment  # if you want to save to DB
from DB.models import SentimentResult, db

youtube_bp = Blueprint("youtube", __name__)

@youtube_bp.route("/sentiment-data/<video_id>")
def sentiment_data(video_id):
    print(f"Sentiment endpoint called for video_id={video_id}")

    # 1. Fetch recent chat messages
    chats = fetch_youtube_chat(video_id, limit=10)
    if not chats:
        print("No chat messages found")
        return jsonify({"positive": 0, "negative": 0, "neutral": 0})

    # 2. Extract just the message texts
    messages = [m["message"] for m in chats]

    # 3. Vectorize messages
    X = vectorizer.transform(messages)

    # 4. Predict sentiments
    preds = model.predict(X)

    # 5. Count sentiments
    pos = sum(1 for p in preds if encoder.inverse_transform([p])[0] == "positive")
    neg = sum(1 for p in preds if encoder.inverse_transform([p])[0] == "negative")
    neu = sum(1 for p in preds if encoder.inverse_transform([p])[0] == "neutral")

    print(f"Predictions → Positive={pos}, Negative={neg}, Neutral={neu}")

    # 6. Store in DB (optional)
    store_sentiment(video_id, pos, neg, neu)

    # 7. Return JSON to frontend
    return jsonify({"positive": pos, "negative": neg, "neutral": neu})
 

@youtube_bp.route("/history", methods=["GET"])
def history_dashboard():
    # Query unique video_ids
    video_ids = db.session.query(SentimentResult.video_id).distinct().all()
    video_ids = [v[0] for v in video_ids]  # unpack tuples
    print(video_ids)
    return render_template("history.html", video_ids=video_ids)

@youtube_bp.route("/history/<video_id>")
def history_chart(video_id):
    # Fetch sentiment records for given video_id
    results = (SentimentResult.query
               .filter_by(video_id=video_id)
               .order_by(SentimentResult.timestamp.asc())
               .all())

    # Convert to dicts for chart.js
    data = {
        "timestamps": [r.timestamp.strftime("%Y-%m-%d %H:%M:%S") for r in results],
        "positive": [r.positive_count for r in results],
        "negative": [r.negative_count for r in results],
        "neutral": [r.neutral_count for r in results]
    }
    return render_template("history_chart.html", video_id=video_id, data=data)
