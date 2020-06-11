from flask import Blueprint, jsonify, request, render_template
from twitter.models import db, Tweet, User, parse_records
from twitter.services.twitter_service import api as twitter_api_client
from twitter.services.basilica_services import connection as basilica_api_client

tweets_route = Blueprint("tweets_route", __name__)

@tweets_route.route("/")
def home():
    return render_template("prediction_form.html")


@tweets_route.route("/tweets.json")
def list_tweets_json():
    
    tweet_records = Tweet.query.all()
    print(tweet_records)
    tweets = parse_records(tweet_records)

    return jsonify(tweets)

@tweets_route.route("/tweets")
def list_tweets():
    
    tweet_records = Tweet.query.all()
    print(tweet_records)
    tweets = parse_records(tweet_records)

    return render_template("tweets.html", message="The tweets that be", tweets=tweets)

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

@tweets_route.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)

    twitter_user = twitter_api_client.get_user(screen_name)
    statuses = twitter_api_client.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    print("STATUSES COUNT:", len(statuses))
 
    # get existing user from the db or initialize a new one:
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()

    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_api_client.embed_sentences(all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS", len(embeddings))

    # TODO: explore using the zip() function maybe...
    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")

        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id
        db_tweet.full_text = status.full_text
        embedding = embeddings[counter]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter+=1
    db.session.commit()

    return render_template("user.html", user=db_user, tweets=statuses)

@tweets_route.route("/users/new")
def new_user():
    return render_template("new_user.html")

@tweets_route.route("/create_user", methods=["POST"])
def create_user(screen_name=None):
    # print("FORM DATA:", dict(request.form))
    screen_name = request.form["user"]
    # print(screen_name)

    twitter_user = twitter_api_client.get_user(screen_name)
    statuses = twitter_api_client.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    print("STATUSES COUNT:", len(statuses))
 
    # get existing user from the db or initialize a new one:
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()

    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_api_client.embed_sentences(all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS", len(embeddings))

    # TODO: explore using the zip() function maybe...
    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")

        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id
        db_tweet.full_text = status.full_text
        embedding = embeddings[counter]
        print(len(embedding))
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter+=1
    db.session.commit()

    return render_template("user.html", user=db_user, tweets=statuses)