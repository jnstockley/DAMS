from src.event.event_model import Events
from src.item.item_model import Items
from src.roles.request_model import Request
from src.roles.donor_model import Donor
from src.event.match_model import Match


def get_events():
    events = Events.query.all()
    return events


def get_requests():
    requests = Request.query.all()
    return requests


def get_donors():
    donors = Donor.query.all()
    return donors


def get_items():
    items = Items.query.all()
    return items


def get_donations():
    donations = Match.query.all()
    return donations


def get_item_categories():
    categories = set(
        [category[0] for category in Items.query.with_entities(Items.category).all()]
    )
    return categories
