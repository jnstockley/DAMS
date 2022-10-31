from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, redirect, url_for, request, flash
from src.account.user_model import User
from src.roles.roles_helper import get_events

donor_blueprint = Blueprint('donor', __name__)


@donor_blueprint.route('/donor')
def show_events():
    events = get_events()
    print(events)
    items = get_items()
    return render_template('donor.html', events = events, items = items)
def get_items():
    items = get_items()


