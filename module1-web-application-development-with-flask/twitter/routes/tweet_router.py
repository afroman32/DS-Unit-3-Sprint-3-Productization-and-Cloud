from flask import Blueprint, jsonify, request, render_template

from twitter.models import db, Tweet, User, parse_records

tweets_route = Blueprint("tweets_route", __name__)


@tweets_route.route("/")
def index():
    x = 2 + 2
    return f"Hello World! {x}"


@tweets_route.route("/tweets.json")
def list_tweets_json():
    
    tweet_records = Tweet.query.all()
    print(tweet_records)
    tweets = parse_records(tweet_records)

    return jsonify(tweets)

@tweets_route.route("/tweets")
def list_tweets():
    
    tweet_records = Tweet.query.all()
    # print(tweet_records)
    books = parse_records(tweet_records)

    return render_template("tweets.html", message="The tweets that be", books=books)

@tweets_route.route("/tweets/new")
def new_tweet():
    return render_template("new_tweet.html")

@tweets_route.route("/tweet/create", methods=["POST"])
def create_tweet():
    print("FORM DATA:", dict(request.form))

    new_tweet = Tweet(content=request.form["content"], user=request.form["User_name"])
    db.session.add(new_tweet)
    db.session.commit()

    return jsonify({
            "message": "Successfully Created (TODO)",
            "book": dict(request.form)
        })