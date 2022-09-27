from src import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
    event_name = db.Column(db.String(100))
    town = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    zipcode = db.Column(db.Integer)
    country_name = db.Column(db.String(3))
    severity_level = db.Column(db.String(100))

