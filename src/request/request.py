from flask import Blueprint

from src.event.event_model import Events
from src.item.item_model import Items

request_blueprint = Blueprint('request', __name__)


def get_events():
    events = Events.query.all()
    return events


def get_items():
    items = Items.query.all()
    return items


@request_blueprint.route("/request")
def add_request():
    return


@request_blueprint.route("/request", methods=['POST'])
def add_request_post():
    return
