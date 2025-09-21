from flask import Blueprint, request, jsonify, render_template
from Utils.url_util import extract_video_id, identify_platform, extract_twitch_channel, extract_youtube_id
from Services.youtube_service import fetch_youtube_chat
from Services.twitch_service import fetch_twitch_chat
from ML.Load_model import model, vectorizer, encoder
from Services.sentiment_service import store_sentiment

common_bp = Blueprint("common", __name__)

@common_bp.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@common_bp.route("/analyze", methods=["POST"])
def analyze():
    url = request.form.get("yt_url")
    platform = identify_platform(url)
    print(f"Platform identified : {platform}")
    if not platform:
        return jsonify({"error": "Unsupported URL"}), 400

    if platform == "youtube":
        video_id = extract_youtube_id(url)
        identifier = video_id
    else:  # twitch
        channel = extract_twitch_channel(url)
        identifier = channel
    print(f"Identifer : {identifier}")
    return render_template("results.html", platform=platform, identifier=identifier)



@common_bp.route("/sentiment-data/<platform>/<identifier>")
def sentiment_data(platform, identifier):
    # Step 1: Fetch messages
    if platform == "youtube":
        chats = fetch_youtube_chat(identifier, limit=10)
    elif platform == "twitch":
        chats = fetch_twitch_chat(identifier, limit=10)
    else:
        return jsonify({"error": "Invalid platform"}), 400

    if not chats:
        return jsonify({"positive": 0, "negative": 0, "neutral": 0})

    # Step 2: Run ML model
    X = vectorizer.transform([m["message"] for m in chats])
    preds = model.predict(X)

    pos = sum(1 for p in preds if encoder.inverse_transform([p])[0] == "positive")
    neg = sum(1 for p in preds if encoder.inverse_transform([p])[0] == "negative")
    neu = sum(1 for p in preds if encoder.inverse_transform([p])[0] == "neutral")

    # Step 3: Store in DB
    store_sentiment(platform, identifier, pos, neg, neu)

    return jsonify({"positive": pos, "negative": neg, "neutral": neu})