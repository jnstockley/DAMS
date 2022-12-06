from src.roles.donor_model import Donor
from src.item.item_model import Items
from src.account.user_model import User
from src.login.login import login_post
from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.roles.roles_helper import get_items, get_donations
from .. import db

donor_blueprint = Blueprint('donor', __name__)


def get_email():
    email = login_post()
    print(email)
    return email



@donor_blueprint.route("/donor-check-shipments")
def donorShipping():
    donations = get_donations()
    return render_template("donor-check-shipments.html", donations=donations)

@donor_blueprint.route("/donor-check-shipments", methods=['POST'])
def donorShipping_post():
    donations = get_donations()
    verified = True
    db.session.query(Match).filter(Match.matchID == matchID).update({'verified': verified})
    db.session.commit()
    flash("Item Changed")

    return render_template("donor-check-shipments.html", donations=donations)

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
    return redirect(url_for("login.donorHome"))
