from re import Pattern

from flask import Blueprint, render_template, redirect, url_for, request, flash
import re
from werkzeug.security import generate_password_hash
from .models import User
from . import db
from . import email_login
from random import randrange

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


@auth.route('/verify-account')
def verify_account():
    return render_template("verify-account.html")


@auth.route('/verify-account', methods=['POST'])
def verify_account_post():
    email = request.form.get("email")
    security_code = request.form.get("security-code")

    account = User.query.filter_by(email=email, security_code=security_code).first()

    if not account:
        flash("Account not found! Email and/or security code are invalid!")
        return redirect(url_for('auth.verify_account'))

    account.verified_email = True
    if account.account_type == "donor":
        account.verified_account = True

    db.session.commit()

    flash("Email verified!")
    return redirect(url_for('auth.verify_account'))


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
        return redirect(url_for('auth.register'))
    if not validate(last_name, NAME_REGEX):
        flash(f'{last_name} is not a valid Last Name!')
        return redirect(url_for('auth.register'))
    if not validate(street_address, STREET_REGEX):
        flash(f'{street_address} is not a valid Street Address!')
        return redirect(url_for('auth.register'))
    if not validate(city, NAME_REGEX):
        flash(f'{city} is not a valid City!')
        return redirect(url_for('auth.register'))
    if not validate(state, STATE_REGEX):
        flash(f'{state} is not a valid State!')
        return redirect(url_for('auth.register'))
    if not validate(zip_code, ZIP_CODE_REGEX):
        flash(f'{zip_code} is not a valid Zip Code!')
        return redirect(url_for('auth.register'))
    if not validate(country, COUNTRY_REGEX):
        flash(f'{country} is not a valid Country!')
        return redirect(url_for('auth.register'))
    if not validate(email, EMAIL_REGEX):
        flash(f'{email} is not a valid Email Address!')
        return redirect(url_for('auth.register'))
    if not password == confirm_password:
        flash("Passwords do not match")
        return redirect(url_for('auth.register'))
    if not validate(password, PASSWORD_REGEX):
        flash("Password must be at least 8 characters and contain at least one number and letter")
        return redirect(url_for('auth.register'))

    user_exists = User.query.filter_by(email=email).first()

    security_code = randrange(100000, 999999)

    while User.query.filter_by(security_code=security_code).first():
        security_code = randrange(100000, 999999)

    if user_exists:
        flash(f'An account with {email} already exists, please sign in!')
        redirect(url_for('auth.register'))

    verified_account = True
    if account_type == 'recipient':
        verified_account = False

    new_user = User(first_name=first_name, last_name=last_name, street_address=street_address, city=city, state=state,
                    country=country, zip=zip_code, email=email, account_password=generate_password_hash(password, method='sha256'), account_type=account_type, verified_account=verified_account, security_code=security_code)

    email_sent = send_verification_email(new_user.email, new_user.security_code)

    if email_sent:
        db.session.add(new_user)
        db.session.commit()
        flash("Please check your email for your security code!")

        return redirect(url_for('auth.verify_account'))

    else:
        flash("Error sending security code email")
        return redirect(url_for('auth.register'))

    # TODO Send email with code, create page for user to input code, validate code and verify email, allow sign in if verified account


def validate(field: str, regex: Pattern[str]):
    return re.fullmatch(regex, field)


def send_verification_email(email: str, security_code):
    import smtplib
    from email.message import EmailMessage

    # create email
    msg = EmailMessage()
    msg['Subject'] = "DAMS Security Code"
    msg['From'] = email_login.username
    msg['To'] = email
    msg.set_content(f"""Hi,
    Your security code is {security_code}
    """)

    # send email
    with smtplib.SMTP_SSL(email_login.smtp, email_login.port) as smtp:
        try:
            smtp.login(email_login.username, email_login.password)
            smtp.send_message(msg)
            return True
        except Exception:
            return False
