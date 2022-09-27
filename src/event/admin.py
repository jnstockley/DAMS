from flask import Blueprint, render_template, redirect, url_for, request, flash

admin_blueprint = Blueprint('admin', __name__)


# this opens the admin main page
@admin_blueprint.route('/admin-home')
def adminHome():
    return render_template("admin-home.html")


# this opens the admin create events page
@admin_blueprint.route('/create-event')
def createEvent():
    return render_template("create-event.html")


'''
@admin_blueprint.route('/createEvent', methods=['POST'])
def createEvent_post():
    #query here
    return render_template("create-event.html")
'''