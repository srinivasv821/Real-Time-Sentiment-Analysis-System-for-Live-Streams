import requests
import config
from ML.Load_model import model, vectorizer, encoder
from Services.sentiment_service import store_sentiment
from datetime import datetime


def get_live_chat_id(video_id):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "id": video_id,
        "part": "liveStreamingDetails",
        "key": config.YOUTUBE_API_KEY
    }
    response = requests.get(url, params=params).json()
    items = response.get("items", [])
    if not items:
        print("No video details found for this video_id")
        return None

    live_details = items[0].get("liveStreamingDetails", {})
    live_chat_id = live_details.get("activeLiveChatId")

    if not live_chat_id:
        print("Video is not live or has no live chat.")
        return None

    return live_chat_id

def fetch_live_chat(live_chat_id, page_token=None):
    url = "https://www.googleapis.com/youtube/v3/liveChat/messages"
    params = {
        "liveChatId": live_chat_id,
        "part": "snippet,authorDetails",
        "key": config.YOUTUBE_API_KEY,
        "pageToken": page_token
    }
    response = requests.get(url, params=params).json()
    return response

def fetch_youtube_chat(video_id, limit=10):
    # step 1: get livechatID from the video
    live_chat_id = get_live_chat_id(video_id)
    if not live_chat_id:
        return None
    # step 2: Get chat messages
    chat_response = fetch_live_chat(live_chat_id)

    messages = []

    for item in chat_response.get("items", []):
        snippet = item.get("snippet", {})
        author = item.get("authorDetails", {}).get("displayName", "Unknown")
        message = snippet.get("displayMessage")  # could be None
        published = snippet.get("publishedAt")

        # Skip system / empty messages
        if not message:
            continue

        messages.append({
            "author": author,
            "message": message,
            "publishedAt": published
        })
    
    return messages[:limit]



def process_batch(video_id, messages):
    # Vectorize
    X = vectorizer.transform([m["message"] for m in messages])
    preds = model.predict(X)
    print(preds)
    # Count sentiment labels
    pos = sum(1 for p in preds if encoder.inverse_transform([p])[0] == "positive")
    neg = sum(1 for p in preds if encoder.inverse_transform([p])[0] == "negative")
    neu = sum(1 for p in preds if encoder.inverse_transform([p])[0] == "neutral")

    # Store in DB
    store_sentiment(video_id, pos, neg, neu)

    return {"video_id": video_id, "positive": pos, "negative": neg, "neutral": neu}
