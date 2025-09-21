from flask import Blueprint, jsonify, request
from Services.twitch_service import fetch_twitch_chat

twitch_bp = Blueprint("twitch", __name__)

@twitch_bp.route("/chat", methods=["GET"])
def get_twitch_chat():
    """
    Example: GET /twitch/chat?channel=shroud&limit=5
    """
    channel = request.args.get("channel")
    limit = request.args.get("limit", default=10, type=int)

    if not channel:
        return jsonify({"error": "channel parameter is required"}), 400

    try:
        chats = fetch_twitch_chat(channel, limit=limit)
        return jsonify(chats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
