from flask import Blueprint, render_template, redirect, url_for, request, flash
from src.event.event_model import Events
from .. import db
from re import Pattern

import re
admin_blueprint = Blueprint('admin', __name__)

admin_createEvent_page = 'admin.createEvent'

# this opens the admin main page
@admin_blueprint.route('/admin-home')
def adminHome():
    return render_template("admin-home.html")


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

    newEvent = Events(event_name=event_name, town=town_name, state=state_name, country=country_name, zipcode=zip_code,
                     severity_level=severity_level)

    db.session.add(newEvent)
    db.session.commit()
    flash("Event Created!")
    return redirect(url_for(admin_createEvent_page))

    #STATE_REGEX = re.compile(r'[a-zA-Z]{2}')