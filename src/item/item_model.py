from src import db


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
    itemName = db.Column(db.String(100))
    category = db.Column(db.String(100))
