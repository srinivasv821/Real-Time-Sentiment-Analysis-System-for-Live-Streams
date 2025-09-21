
# this is a test program to fetch live chat from youtube live stream
import requests
import time

API_KEY = "API_key_here"
VIDEO_ID = "adHRJuob-2o"

# Step 1: Get the liveChatId for the video
def get_live_chat_id(video_id):
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "id": video_id,
        "part": "liveStreamingDetails",
        "key": API_KEY
    }
    response = requests.get(url, params=params).json()
    items = response.get("items", [])
    if not items:
        raise Exception("No live stream found for this video_id.")
    return items[0]["liveStreamingDetails"]["activeLiveChatId"]

# Step 2: Fetch live chat messages
def fetch_live_chat(live_chat_id, page_token=None):
    url = "https://www.googleapis.com/youtube/v3/liveChat/messages"
    params = {
        "liveChatId": live_chat_id,
        "part": "snippet,authorDetails",
        "key": API_KEY,
        "pageToken": page_token
    }
    response = requests.get(url, params=params).json()
    return response

def main():
    live_chat_id = get_live_chat_id(VIDEO_ID)
    print(f"Connected to Live Chat ID: {live_chat_id}")

    next_page_token = None
    while True:
        chat_response = fetch_live_chat(live_chat_id, next_page_token)

        for item in chat_response.get("items", []):
            snippet = item["snippet"]
            author = item["authorDetails"]["displayName"]
             # Normal text message
            if snippet["type"] == "textMessageEvent":
                print(f"{author}: {snippet.get('displayMessage')}")
            
            # # Super Chat
            # elif snippet["type"] == "superChatEvent":
            #     amount = snippet.get("superChatDetails", {}).get("amountDisplayString")
            #     print(f"{author} sent a Super Chat: {amount}")
            
            # # Other types (membership, etc.)
            # else:
            #     print(f"{author} sent a {snippet['type']}")

        # Get token for next page
        next_page_token = chat_response.get("nextPageToken")

        # Wait according to polling interval (Google recommends this!)
        time.sleep(chat_response.get("pollingIntervalMillis", 2000) / 1000.0)

if __name__ == "__main__":
    main()
