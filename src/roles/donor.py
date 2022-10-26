from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, redirect, url_for, request, flash
from src.account.user_model import User

donor_blueprint = Blueprint('donor', __name__)

@donor_blueprint.route('/home')
def fetch_events():
	return render_template('home.html')

