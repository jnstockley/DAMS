from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullabe=False)  # primary keys are required by SQLAlchemy
    first_name = db.Column(db.String(100), nullabe=False)
    last_name = db.Column(db.String(100), nullabe=False)
    street_address = db.Column(db.String(100), nullabe=False)
    city = db.Column(db.String(100), nullabe=False)
    state = db.Column(db.String(2), nullabe=False)
    country = db.Column(db.String(3), nullabe=False)
    zip = db.Column(db.Integer, nullabe=False)
    email = db.Column(db.String(100), unique=True, nullabe=False)
    password = db.Column(db.String(100), nullabe=False)
    account_type = db.Column(db.String(100), nullabe=False)  # TODO Needs to be improved
    verified_email = db.Column(db.Boolean, default=False)
    admin_account = db.Column(db.Boolean, default=False)
