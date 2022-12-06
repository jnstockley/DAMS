from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, redirect, url_for, request, flash
from src.account.user_model import User
from src.roles.roles_helper import get_events
from src.roles.roles_helper import get_items
from flask_login import LoginManager

login_blueprint = Blueprint('login', __name__)

login_manager = LoginManager()


@login_blueprint.route('/home')
def home():
    return render_template('home.html')


@login_blueprint.route('/login')
def login():
    return render_template('login.html')

@login_blueprint.route("/donor-home")
def donorHome():
    return render_template("donor-home.html")
@login_blueprint.route('/donor')
def donor():
    items = get_items()
    return render_template('donor.html', items=items)


@login_blueprint.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.account_password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login.login'))  # if the user doesn't exist or password is wrong, reload the page

    if user.admin_account:
        return redirect(url_for('admin.adminHome'))
    else:
        if user.verified_email:
            print('User email is verified')
            if user.account_type == 'donor':
                print('User account type is donor.')
                return redirect(url_for('login.donor'))
            elif user.account_type == 'recipient':
                print('User account type is recipient.')
                return redirect(url_for('recipient.add_request'))
        else:
            return render_template('verify-account.html')

    return email, render_template('login.html')


@login_blueprint.route('/verifying_credentials', methods=['POST'])
def verifyingCredentials():
    return render_template('verifying_credentials.html')


@login_blueprint.route('/recipient')
def recipient():
    return render_template('recipient.html')


@login_blueprint.route('/login', methods=['POST'])
def verifying_user_type():
    email = request.form.get('email')
    password = request.form.get('password')
    # remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.account_password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login.login'))  # if the user doesn't exist or password is wrong, reload the page

    if user.admin_account:
        return redirect(url_for('admin.adminHome'))
    else:
        if user.verified_email:
            print('User email is verified')
            if user.verified_account:
                print('User account is verified')
                if user.account_type == 'donor':
                    print('User account type is donor.')
                    return show_events()
                elif user.account_type == 'recipient':
                    print('User account type is recipient.')
                    return render_template('recipient.html')
            else:
                return render_template('verifying_credentials.html')
        else:
            return render_template('verify-account.html')


@login_blueprint.route('/forgot_password')
def forgot_password():
    return render_template('verify-account')


@login_blueprint.route('/logout')
def logout():
    logout_user()
    return render_template('login.html')
