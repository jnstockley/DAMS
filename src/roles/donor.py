from src.roles.donor_model import Donor
from src.item.item_model import Items
from src.account.user_model import User
from src.login.login import login_post
from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.roles.roles_helper import get_items
from .. import db

donor_blueprint = Blueprint('donor', __name__)


def get_email():
    email = login_post()
    print(email)
    return email



@donor_blueprint.route("/donor-check-shipments")
def donorShipping():
    return redirect(url_for("donor-check-shipments"))

@donor_blueprint.route("/donor-home")
def donorHome():
    return render_template("donor-home.html")


@donor_blueprint.route("/donor", methods=['POST'])
def add_donor_post():
    item = get_items()

    quantity = request.form['quantity']
    items = request.form['item']

    request_db = Donor(itemID=items, quantity=quantity, email='vinaypursnani@icloud.com')

    db.session.add(request_db)

    db.session.commit()

    flash("Donation Request Received!")
    return redirect(url_for("login.donor"))
