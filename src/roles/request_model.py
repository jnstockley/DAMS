from src import db


class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
    eventID = db.Integer #db.column(db.Integer(), db.ForeignKey("events.eventID"))
    itemQuantityID = db.Integer #db.column(db.Integer(), db.ForeignKey("items.id"))
