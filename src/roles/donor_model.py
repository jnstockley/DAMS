from src import db

class Donor(db.Model):
    donorID = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100))
    itemID = db.Column(db.Integer)
    quantity = db.Column(db.Integer)


