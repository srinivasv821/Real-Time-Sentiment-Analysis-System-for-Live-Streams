from urllib.parse import urlparse, parse_qs

def identify_platform(url):
    parsed = urlparse(url)

    if "youtube.com" in parsed.hostname or "youtu.be" in parsed.hostname:
        return "youtube"
    elif "twitch.tv" in parsed.hostname:
        return "twitch"
    return None


def extract_youtube_id(url):
    parsed = urlparse(url)
    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed.query).get("v", [None])[0]
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    return None


def extract_twitch_channel(url):
    parsed = urlparse(url)
    if "twitch.tv" in parsed.hostname:
        return parsed.path.strip("/")
    return None



def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed_url.query).get("v", [None])[0]
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    return None
