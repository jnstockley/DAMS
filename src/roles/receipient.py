from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.roles.roles_helper import get_events, get_items
from src.event.event_model import Events
from src.item.item_model import Items
from src.roles.request_model import Requests
from .. import db


request_blueprint = Blueprint('donor', __name__)


@request_blueprint.route("/request")
def add_request():
    events = get_events()
    items = get_items()
    return render_template('recipient.html', events=[event.event_name for event in events], items=[item.itemName for
                                                                                                   item in items])


@request_blueprint.route("/request", methods=['POST'])
def add_request_post():
    event = Events.query.filter_by(event_name=request.form.get("event")).first()
    items = Items.query.filter(Items.itemName.in_(request.form.getlist("items"))).all()

    print(event.eventID)

    print(items[0].id)

    item_request = Requests()#(eventID=event.eventID, itemQuantityID=items[0].id)

    item_request.eventID = event.eventID
    item_request.itemQuantityID = items[0].id

    db.session.add(item_request)
    db.session.commit()

    flash("Linked item(s) with event")
    return redirect(url_for("login.login"))

