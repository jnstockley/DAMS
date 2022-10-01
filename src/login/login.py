from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, redirect, url_for, request, flash
from src.account.user_model import User

login_blueprint = Blueprint('login', __name__)

VERIFY_ACCOUNT_PAGE = 'register.verify_account'
REGISTER_ACCOUNT_PAGE = 'register.register'
VERIFY_CREDENTIALS_PAGE = 'login.verifyingCredentials'
LOGIN_PAGE = 'login.login'
DONOR_PAGE = 'login.donor'
RECIPIENT_PAGE = 'login.recipient'


@login_blueprint.route('/login')
def login():
    return render_template('login.html')


@login_blueprint.route('/verifying_credentials', methods=['POST'])
def verifyingCredentials():
    return render_template('verifying_credentials.html')


@login_blueprint.route('/donor')
def donor():
    return render_template('donor.html')


@login_blueprint.route('/recipient')
def donor():
    return render_template('recipient.html')


@login_blueprint.route('/login', methods=['POST'])
def verifying_user_type():
    email = request.form.get('email')
    password = request.form.get('password')
    # remember = True if request.form.get('remember') else False
    print(password)
    user = User.query.filter_by(email=email).first()
    print(user.account_password)
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.account_password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login.login'))  # if the user doesn't exist or password is wrong, reload the page

    if user.admin_account:
        return redirect(url_for('admin.adminHome'))
    else:
        if user.verified_email:
            if user.verified_account:
                if user.account_type == 'donor':
                    return redirect(url_for(DONOR_PAGE))
                elif user.account_type == 'recipient':
                    return redirect(url_for(RECIPIENT_PAGE))
            else:
                return redirect(url_for(VERIFY_CREDENTIALS_PAGE))
        else:
            return redirect(url_for(VERIFY_ACCOUNT_PAGE))

    return redirect(url_for(LOGIN_PAGE))
