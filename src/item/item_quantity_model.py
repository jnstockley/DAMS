from src import db


class ItemQuantity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    request_id = db.Column(db.Integer, nullable=False)
