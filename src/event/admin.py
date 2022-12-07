from flask import Blueprint, render_template, request, flash
from src.event.event_model import Events
from src.item.item_model import Items
from src.roles.roles_helper import get_items, get_requests, get_donors, get_events
from .match_model import Match

from .. import db, emailCreds

from ..roles.donor_model import Donor
from ..roles.request_model import Request

admin_blueprint = Blueprint("admin", __name__)

admin_createEvent_page = "admin.createEvent"
admin_createItem_page = "admin.createItem"

modify_item = "modify_item.html"
delete_item = "delete_item.html"
create_item = "create_item.html"
create_event = "create-event.html"


# this opens the admin main page
@admin_blueprint.route("/admin-home")
def admin_home():
    return render_template("admin-home.html")


##################################################################
# this opens admin match items page
@admin_blueprint.route("/match-requests")
def match_requests():
    requests = get_requests()
    donors = get_donors()
    items = get_items()
    events = get_events()

    return render_template(
        "match_requests.html",
        requests=requests,
        donors=donors,
        items=items,
        events=events,
    )


@admin_blueprint.route("/match-requests", methods=["POST"])
def match_requests_post():
    request_data = request.form.to_dict()["requestVal"]

    donor_data = request.form.to_dict()["donorVal"]

    match = Match()

    match.requestID = request_data

    match.donorID = donor_data

    db.session.add(match)

    db.session.commit()

    request_item = (
        db.session.query(Request).filter(Request.requestID == request_data).first()
    )

    donor_item = db.session.query(Donor).filter(Donor.donorID == request_data).first()

    email = donor_item.email

    event_id = request_item.eventID

    event = db.session.query(Events).filter(Events.eventID == event_id).first()

    address = f"{event.town}, {event.state} {event.zipcode} {event.country}"

    send_match_email(email, address)

    return match_requests()


##################################################################

# this opens admin modify events page
@admin_blueprint.route("/modify-item")
def modify_item():
    items = get_items()

    return render_template("modify_item.html", items=[item.itemName for item in items])


# this modifies an item and changes it in database
@admin_blueprint.route("/modify-item", methods=["POST"])
def modify_item_post():
    item_name = request.form.get("itemVal")
    item_name2 = request.form.get("item-name2")
    category = request.form.get("category")

    if db.session.query(Items).filter(Items.itemName == item_name).count():
        if (
                db.session.query(Items).filter(Items.itemName == item_name2).count()
                and item_name != item_name2
        ):
            flash("The item you want to change to already exists")
            return render_template(modify_item)
        else:
            db.session.query(Items).filter(Items.itemName == item_name).update(
                {"itemName": item_name2, "category": category}
            )
            db.session.commit()
            flash("Item Changed")
            return render_template(modify_item)
    else:
        flash("The item you are trying to change does not exist")
        return render_template(modify_item)


####################################################################


# this opens admin delete item page
@admin_blueprint.route("/delete-item")
def delete_item():
    items = get_items()

    return render_template("delete_item.html", items=[item.itemName for item in items])


# delete item
@admin_blueprint.route("/delete-item", methods=["POST"])
def delete_item_post():
    item_name = request.form.get("itemVal")

    if db.session.query(Items).filter(Items.itemName == item_name).count():
        Items.query.filter(Items.itemName == item_name).delete()
        db.session.commit()
        flash("Item Deleted!")
        return render_template(delete_item)
    else:
        flash("Item does not exist!")
        return render_template(delete_item)


###################################################################

# opens the create items page
@admin_blueprint.route("/create-item")
def create_item():
    return render_template("create_item.html")


# creates an item and adds to database
@admin_blueprint.route("/create-item", methods=["POST"])
def create_item_post():
    item_name = request.form.get("item-name")
    category = request.form.get("category")

    if db.session.query(Items).filter(Items.itemName == item_name).count():
        flash("Item already exits!")
        return render_template(create_item)

    else:
        new_item = Items(itemName=item_name, category=category)

        db.session.add(new_item)
        db.session.commit()
        flash("Item Created!")
        return render_template(create_item)


###################################################################


# this opens the admin create events page
@admin_blueprint.route("/create-event")
def create_event():
    return render_template("create-event.html")


# for getting info from boxes to send to database
@admin_blueprint.route("/create-event", methods=["POST"])
def create_event_post():
    # query here, getting all textbox info from webpage
    event_name = request.form.get("event-name")
    town_name = request.form.get("town-name")
    state_name = request.form.get("state-name")
    country_name = request.form.get("country-name")
    zip_code = request.form.get("zipcodeNum")
    severity_level = request.form.get("severity-level")

    if db.session.query(Events).filter(Events.event_name == event_name).count():
        flash("Event already exits!")
        return render_template(create_event)
    else:

        new_event = Events(
            event_name=event_name,
            town=town_name,
            state=state_name,
            country=country_name,
            zipcode=zip_code,
            severity_level=severity_level,
        )

        db.session.add(new_event)
        db.session.commit()
        flash("Event Created!")
        return render_template(create_event)


def send_match_email(email, address):
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg["Subject"] = "DAMS Match"
    msg["From"] = emailCreds.username
    msg["To"] = email
    msg.set_content(
        f"""Hi,
    Your donation has been matched, be send the requested items to:
    {address}
    Thank you!"""
    )

    with smtplib.SMTP_SSL(emailCreds.smtp, emailCreds.port) as smtp:
        try:
            smtp.login(emailCreds.username, emailCreds.password)
            smtp.send_message(msg)
        except smtplib.SMTPException:
            print("Email not sent")
