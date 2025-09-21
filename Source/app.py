from flask import Flask
from Api.youtube_routes import youtube_bp
from Api.twitch_routes import twitch_bp
from Api.common_routes import common_bp
from DB.models import db
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__, template_folder='templates')

    # Flask Migration setup
    migrate = Migrate(app, db)
    # Configure Postgres
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/live_sentiment"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Init SQLAlchemy
    db.init_app(app)
    with app.app_context():
        db.create_all()
    #Register blueprints
    app.register_blueprint(youtube_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(twitch_bp)
    # app.register_blueprint(twitch_bp, url_prefix="/twitch")

    return app

# Test region - Start
# app = Flask(__name__)
# from Services.youtube_service import fetch_youtube_chat
# from flask import jsonify
# @app.route('/')
# def home():
#     chats = fetch_youtube_chat(video_id="tXRuaacO-ZU")
#     return jsonify({"messages": chats})

# if __name__ == '__main__':
#     app.run(debug=True)

# Test region - End

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)