from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.roles.roles_helper import get_events, get_items
from src.item.item_quantity_model import ItemQuantity
from src.roles.request_model import Request
from .. import db


request_blueprint = Blueprint('recipient', __name__)


@request_blueprint.route("/request")
def add_request():
    events = [event for event in get_events()]
    items = get_items()

    all_categories = ["food", "utilities", "vaccine", "clothing", "money"]

    data = {}
    max_items = 0
    for category in all_categories:
        item_list = []
        num_items = 0
        for item in items:
            if item.category == category:
                item_list.append(item.itemName.capitalize())
                num_items += 1
            if max_items < num_items:
                max_items = num_items
            data[category] = item_list

    return render_template('recipient.html', events=events, table_dict=data, max_items=max_items)


@request_blueprint.route("/request", methods=['POST'])
def add_request_post():

    items = get_items()

    item_ids = {item.itemName.lower(): item.id for item in items}

    item_names = [item.itemName.lower() for item in items]

    data = request.form.to_dict()

    item_quantity = {item_ids[item]: int(data[item]) for item in item_names if int(data[item].lower()) > 0}

    request_db = Request()

    db.session.add(request_db)
    db.session.commit()

    for item_pair in item_quantity:
        db.session.add(
            ItemQuantity(item_id=int(item_pair), quantity=item_quantity[item_pair], request_id=request_db.id))
    db.session.commit()

    flash("Successfully added request, and linked items to event!")
    return redirect(url_for("donor.add_request"))