import os
import smtplib
import random
import string
from flask_mail import Mail, Message
from flask import Flask, render_template, request, g, redirect, session, url_for, Blueprint
from flask_mysqldb import MySQL
from werkzeug import check_password_hash, generate_password_hash
# Database
from GSN import database
from flask_uploads import UploadSet, configure_uploads, IMAGES


mod = Blueprint('application', __name__, template_folder='templates')


# Mmoding on home page
@mod.route("/")
def index():
    if g.user:
        return render_template("Map.html")
    else:
        return render_template("Registration.html")


@mod.route("/all", methods = ["GET"])
def showAll():
    users = database.Users.query.all()
    toShow = ""
    for user in users:
        toShow += str(user.user_id)  + "||" + str(user.login) + "||" + str(user.email) + "||" + str(user.password) + "||" + str(user.activation_link) + "<br>"
    if users is None:
        return None
    return toShow



