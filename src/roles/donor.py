from src.roles.donor_model import Donor
from src.item.item_model import Items
from src.login.login import login_post
from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.roles.roles_helper import get_donations
from .request_model import Request
from .. import db
from ..event.event_model import Events
from ..event.match_model import Match

donor_blueprint = Blueprint("donor", __name__)


def get_email():
    email = login_post()
    print(email)
    return email


@donor_blueprint.route("/donor-check-shipments")
def donor_shipping():
    donations = get_donations()

    donors = dict()
    for donor in donations:
        donor_id = (
            db.session.query(Donor)
            .filter(Donor.donorID == donor.donorID)
            .first()
            .itemID
        )
        donors[donor_id] = db.session.query(Items).filter(Items.id == donor_id).first().itemName

    return render_template("donor-check-shipments.html", donations=donors)


@donor_blueprint.route("/donor-check-shipments", methods=["POST"])
def donor_shipping_post():

    item_id = request.form.to_dict()["donation"]

    donor_id = db.session.query(Donor).filter(Donor.itemID == item_id).first().donorID

    match = db.session.query(Match).filter(Match.donorID == donor_id).first()

    match.verified = True

    db.session.commit()

    flash("Item Verification Updated!")

    return redirect("donor-check-shipments")


@donor_blueprint.route("/donor_home")
def donor_home():
    items = db.session.query(Request).all()
    return render_template("donor-home.html", items=items, db=db, Events=Events, Items=Items)


@donor_blueprint.route("/donor", methods=["POST"])
def add_donor_post():
    quantity = request.form["quantity"]
    items = request.form["item"]

    request_db = Donor(
        itemID=items, quantity=quantity, email="vinaypursnani@icloud.com"
    )

    db.session.add(request_db)

    db.session.commit()

    flash("Donation Request Received!")
    return redirect(url_for("login.donorHome"))
