from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # primary keys are required by SQLAlchemy
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    street_address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    country = db.Column(db.String(3))
    zip = db.Column(db.Integer)
    email = db.Column(db.String(100), unique=True)
    account_password = db.Column(db.String(100))
    account_type = db.Column(db.String(100))  # TODO Needs to be improved
    verified_email = db.Column(db.Boolean, default=False)
    verified_account = db.Column(db.Boolean, default=True)
    admin_account = db.Column(db.Boolean, default=False)
    security_code = db.Column(db.Integer, unique=True)
