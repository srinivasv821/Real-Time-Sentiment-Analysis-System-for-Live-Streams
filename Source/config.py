import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# YouTube Config
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Twitch Config
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_SECRET = os.getenv("TWITCH_SECRET")
TWITCH_ACCESS_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")
TWITCH_REFRESH_TOKEN = os.getenv("TWITCH_REFRESH_TOKEN")
TWITCH_NICK=os.getenv("TWITCH_NICK")
