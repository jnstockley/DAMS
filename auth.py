from re import Pattern

from flask import Blueprint, render_template, redirect, url_for, request, flash
import re
from werkzeug.security import generate_password_hash
from .models import User
from . import db

NAME_REGEX = re.compile(r'[a-zA-Z]{3,100}')
EMAIL_REGEX = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
STREET_REGEX = re.compile(r'\w+(\s\w+){2,}')
STATE_REGEX = re.compile(r'[a-zA-Z]{2}')
ZIP_CODE_REGEX = re.compile(r'[0-9]{5}')
COUNTRY_REGEX = re.compile(r'[a-zA-Z]{2,3}')
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

auth = Blueprint('auth', __name__)


@auth.route('/register')
def register():
    return render_template("register.html")


@auth.route('/register', methods=['POST'])
def register_post():
    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")

    street_address = request.form.get("street-address")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip-code")
    country = request.form.get("country")

    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm-password")

    account_type = request.form.get("account-type")

    if not validate(first_name, NAME_REGEX):
        flash(f'{first_name} is not a valid First Name!')
    if not validate(last_name, NAME_REGEX):
        flash(f'{last_name} is not a valid Last Name!')
    if not validate(street_address, STREET_REGEX):
        flash(f'{street_address} is not a valid Street Address!')
    if not validate(city, NAME_REGEX):
        flash(f'{city} is not a valid City!')
    if not validate(state, STATE_REGEX):
        flash(f'{state} is not a valid State!')
    if not validate(zip_code, ZIP_CODE_REGEX):
        flash(f'{zip_code} is not a valid Zip Code!')
    if not validate(country, COUNTRY_REGEX):
        flash(f'{country} is not a valid Country!')
    if not validate(email, EMAIL_REGEX):
        flash(f'{email} is not a valid Email Address!')
    if not password == confirm_password:
        flash("Passwords do not match")
    if not validate(password, PASSWORD_REGEX):
        flash("Password must be at least 8 characters and contain at least one number and letter")

    user_exists = User.query.filter_by(email=email).first()

    if user_exists:
        flash(f'An account with {email} already exists, please sign in!')
        redirect(url_for('auth.register'))

    new_user = User(first_name=first_name, last_name=last_name, street_address=street_address, city=city, state=state,
                    country=country, zip=zip_code, email=email, account_password=generate_password_hash(password, method='sha256'), account_type=account_type)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.register'))


def validate(field: str, regex: Pattern[str]):
    return re.fullmatch(regex, field)
