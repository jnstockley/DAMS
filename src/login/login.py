from flask import Blueprint, render_template, redirect, url_for, request, flash
from src.event.event_model import Events
from .. import db
from re import Pattern
from werkzeug.security import generate_password_hash
from src.account.user_model import User

import re

login_blueprint = Blueprint('login', __name__)

VERIFY_ACCOUNT_PAGE = 'register.verify_account'
REGISTER_ACCOUNT_PAGE = 'register.register'


@admin_blueprint.route('/login')
def login():
    return render_template('login.html')


@admin_blueprint.route('/verifying_user_type')
def verifying_user_type():
    email = request.form.get("email")
    password = request.form.get("password")

    hashedPassword = generate_password_hash(password, method='sha256')

    account = User.query.filter_by(email=email, password=hashedPassword).first()

    user_exists = User.query.filter_by(email=email).first()

    if user_exists:
        if account.password == hashedPassword:
            if account.admin_account == 1:
                return render_template('admin.py')
            else:
                if account.verified_account == 1:
                    if account.account_type == "donor":
                        return render_template('donor.html')
                    elif account.account_type == "receipent":
                        return render_template == ('receipent.html')
                else:
                    render_template(url_for(VERIFY_ACCOUNT_PAGE))
        else:
            flash('Please verify your credentials!')
    else:
        render_template(url_for(REGISTER_ACCOUNT_PAGE))