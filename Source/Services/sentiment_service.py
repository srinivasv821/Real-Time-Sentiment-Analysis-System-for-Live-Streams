from DB.models import db, SentimentResult
from datetime import datetime

def store_sentiment(platform, video_id, pos, neg, neu):
    result = SentimentResult(
        platform=platform,
        video_id=video_id,
        positive_count=pos,
        negative_count=neg,
        neutral_count=neu
    )
    db.session.add(result)
    db.session.commit()
    print(f"{platform} | Stored sentiment for {video_id} at {result.timestamp}: P={pos}, N={neg}, Neu={neu}")
