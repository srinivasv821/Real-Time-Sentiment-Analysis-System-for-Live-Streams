from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import text

db = SQLAlchemy()

class SentimentResult(db.Model):
    __tablename__ = "sentiment_results"

    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(20),nullable=False,default="youtube",server_default=text("'youtube'"))
    video_id = db.Column(db.String(50), nullable=False)     # YouTube video_id OR Twitch channel
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    positive_count = db.Column(db.Integer, default=0)
    negative_count = db.Column(db.Integer, default=0)
    neutral_count = db.Column(db.Integer, default=0)
