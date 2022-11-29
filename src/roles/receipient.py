from flask import Blueprint, render_template, request, flash, redirect, url_for
from src.roles.roles_helper import get_events, get_items
from src.roles.request_model import Request
from .. import db


request_blueprint = Blueprint('recipient', __name__)


@request_blueprint.route("/request")
def add_request():
    events = get_events()
    items = get_items()

    '''all_categories = ["food", "utilities", "vaccine", "clothing", "money"]

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
            data[category] = item_list'''

    return render_template('recipient.html', events=events, items=items)


@request_blueprint.route("/request", methods=['POST'])
def add_request_post():

    event = request.form['event']

    item = request.form['item']

    quantity = request.form['quantity']

    request_db = Request(itemID=item, eventID=event, quantity=quantity)

    db.session.add(request_db)

    db.session.commit()

    flash("Successfully added request, and linked items to event!")
    return redirect(url_for("recipient.add_request"))
