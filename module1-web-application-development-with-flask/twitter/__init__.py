from flask import Flask

from twitter.models import db, migrate
from twitter.routes.tweet_router import tweets_route
from twitter.routes.stats_routes import stats_routes

DATABASE_URI = "sqlite:///twitter_app.db" # using relative filepath

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(tweets_route)
    app.register_blueprint(stats_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)