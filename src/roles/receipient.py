from flask import Blueprint, render_template, request
from src.roles.roles_helper import get_events, get_items

request_blueprint = Blueprint('donor', __name__)


@request_blueprint.route("/request")
def add_request():
    events = get_events()
    items = get_items()
    return render_template('recipient.html', events=[event.event_name for event in events], items=[item.itemName for
                                                                                                   item in items])


@request_blueprint.route("/request", methods=['POST'])
def add_request_post():
    event = request.form.get("event")
    items = request.form.getlist("items")
    return {"Event": event, "Items": items}
