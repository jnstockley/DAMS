from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.roles.roles_helper import get_events, get_items, get_item_categories
from src.item.item_quantity_model import ItemQuantity
from src.roles.request_model import Request
from .. import db
from collections import OrderedDict


request_blueprint = Blueprint('donor', __name__)


@request_blueprint.route("/request")
def add_request():
    events = [event for event in get_events()]
    items = get_items()
    categories = get_item_categories()

    data = {}
    for category in categories:
        items_list = []
        for item in items:
            if item.category == category:
                items_list.append(item.itemName.capitalize())
        data[category.capitalize()] = items_list

    for dict_items in data:
        for c, i in dict_items.items():
            print(c)

    return render_template('recipient.html', events=events, data=OrderedDict(sorted(data.items())), categories=categories)


@request_blueprint.route("/request", methods=['POST'])
def add_request_post():

    items = get_items()

    item_ids = {item.itemName: item.id for item in items}

    item_names = [item.itemName for item in items]

    data = request.form.to_dict()

    item_quantity = {item_ids[item]: int(data[item]) for item in item_names if int(data[item]) > 0}

    request_db = Request()

    db.session.add(request_db)
    db.session.commit()

    for item_pair in item_quantity:
        print(int(item_pair), item_quantity[item_pair])
        db.session.add(ItemQuantity(item_id=int(item_pair), quantity=item_quantity[item_pair], request_id=request_db.id))
    db.session.commit()

    flash("Successfully added request, and linked items to event!")
    return redirect(url_for("admin.createEvent"))
