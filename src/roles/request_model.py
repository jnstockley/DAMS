from src import db


class Request(db.Model):
    requestID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
    itemID = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    eventID = db.Column(db.Integer)