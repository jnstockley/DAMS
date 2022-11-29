from flask import Blueprint, render_template, redirect, url_for, request, flash
from src.event.event_model import Events
from src.item.item_model import Items
from src.roles.roles_helper import get_items, get_requests

from .. import db
from re import Pattern

import re

admin_blueprint = Blueprint('admin', __name__)

admin_createEvent_page = 'admin.createEvent'
admin_createItem_page = 'admin.createItem'


# this opens the admin main page
@admin_blueprint.route('/admin-home')
def adminHome():
    return render_template("admin-home.html")


##################################################################
# this opens admin match items page
@admin_blueprint.route('/match-requests')
def matchRequests():
    requests = get_requests()

    return render_template("match_requests.html", requests=requests)


@admin_blueprint.route('/match-requests', methods=['POST'])
def matchRequestsPost():

    return render_template("match_requests.html", requests=requests)

##################################################################

# this opens admin modify events page
@admin_blueprint.route('/modify-item')
def modifyItem():
    items = get_items()

    return render_template("modify_item.html", items=[item.itemName for item in items])


# this modifies an item and changes it in database
@admin_blueprint.route('/modify-item', methods=['POST'])
def modifyItem_post():
    item_name = request.form.get("itemVal")
    item_name2 = request.form.get("item-name2")
    category = request.form.get("category")

    if db.session.query(Items).filter(Items.itemName == item_name).count():
        if db.session.query(Items).filter(Items.itemName == item_name2).count() and item_name != item_name2:
            flash("The item you want to change to already exists")
            return render_template("modify_item.html")
        else:
            db.session.query(Items).filter(Items.itemName == item_name).update({'itemName': item_name2, 'category' : category})
            db.session.commit()
            flash("Item Changed")
            return render_template("modify_item.html")
    else:
        flash("The item you are trying to change does not exist")
        return render_template("modify_item.html")


####################################################################


# this opens admin delete item page
@admin_blueprint.route('/delete-item')
def deleteItem():
    items = get_items()

    return render_template("delete_item.html", items=[item.itemName for item in items])


# delete item
@admin_blueprint.route('/delete-item', methods=['POST'])
def deleteItem_post():
    item_name = request.form.get("itemVal")

    if db.session.query(Items).filter(Items.itemName == item_name).count():
        Items.query.filter(Items.itemName == item_name).delete()
        db.session.commit()
        flash("Item Deleted!")
        return render_template("delete_item.html")
    else:
        flash("Item does not exist!")
        return render_template("delete_item.html")



###################################################################

# opens the create items page
@admin_blueprint.route('/create-item')
def createItem():
    return render_template("create_item.html")


# creates an item and adds to database
@admin_blueprint.route('/create-item', methods=['POST'])
def createItem_post():
    item_name = request.form.get("item-name")
    category = request.form.get("category")

    if db.session.query(Items).filter(Items.itemName == item_name).count():
        flash("Item already exits!")
        return render_template("create_item.html")

    else:
        newItem = Items(itemName=item_name, category=category)

        db.session.add(newItem)
        db.session.commit()
        flash("Item Created!")
        return render_template("create_item.html")

    # return 0;


###################################################################


# this opens the admin create events page
@admin_blueprint.route('/create-event')
def createEvent():
    return render_template("create-event.html")


# for getting info from boxes to send to database
@admin_blueprint.route('/create-event', methods=['POST'])
def createEvent_post():
    # query here, getting all textbox info from webpage
    event_name = request.form.get("event-name")
    town_name = request.form.get("town-name")
    state_name = request.form.get("state-name")
    country_name = request.form.get("country-name")
    zip_code = request.form.get("zipcodeNum")
    severity_level = request.form.get("severity-level")

    if db.session.query(Events).filter(Events.event_name == event_name).count():
        flash("Event already exits!")
        return render_template("create-event.html")
    else:

        newEvent = Events(event_name=event_name, town=town_name, state=state_name, country=country_name, zipcode=zip_code,
                      severity_level=severity_level)

        db.session.add(newEvent)
        db.session.commit()
        flash("Event Created!")
        return render_template("create-event.html")

    # STATE_REGEX = re.compile(r'[a-zA-Z]{2}')
