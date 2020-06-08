from flask import Flask

from twitter.models import db, migrate
from twitter.routes.tweet_router import tweets_route
# from web_app.routes.book_routes import book_routes

DATABASE_URI = "sqlite:///twitter_app.db" # using relative filepath
#DATABASE_URI = "sqlite:////Users/Username/Desktop/your-repo-name/web_app_99.db" # using absolute filepath on Mac (recommended)
#DATABASE_URI = "sqlite:///C:\\Users\\Username\\Desktop\\your-repo-name\\web_app_99.db" # using absolute filepath on Windows (recommended) h/t: https://stackoverflow.com/a/19262231/670433


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    db.init_app(app)
    migrate.init_app(app, db)

    # app.register_blueprint(home_routes)
    app.register_blueprint(tweets_route)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)