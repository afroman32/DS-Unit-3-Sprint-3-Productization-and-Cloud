# web_app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128))
    user = db.Column(db.String(128))

    def __repr__(self):
        return f"<Tweet {self.id} {self.content}>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(128))

    def __repr__(self):
        return f"<Tweet {self.id} {self.user}>"
    
def parse_records(database_records):
    """
    A helper method for converting a list of database record objects into a list of dictionaries, so they can be returned as JSON

    Param: database_records (a list of db.Model instances)

    Example: parse_records(User.query.all())

    Returns: a list of dictionaries, each corresponding to a record, like...
        [
            {"id": 1, "title": "Book 1"},
            {"id": 2, "title": "Book 2"},
            {"id": 3, "title": "Book 3"},
        ]
    """
    parsed_records = []
    for record in database_records:
        print(record)
        parsed_record = record.__dict__
        del parsed_record["_sa_instance_state"]
        parsed_records.append(parsed_record)
    return parsed_records