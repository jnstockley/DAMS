from src import db


class Donor(db.Model):
    donorID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(45))
    requestID = db.Column(db.Integer)
    amount = db.Column(db.Integer)
