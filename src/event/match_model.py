from src import db


class Match(db.Model):
    matchID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
    requestID = db.Column(db.Integer)
    donorID = db.Column(db.Integer)
