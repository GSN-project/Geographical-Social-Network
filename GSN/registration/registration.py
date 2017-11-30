import os
import smtplib
from flask_mail import Mail, Message
from flask import Flask, render_template, request, g, redirect, session, url_for, Blueprint
from werkzeug import check_password_hash, generate_password_hash
import random
import string
from flask_uploads import UploadSet, configure_uploads, IMAGES
# Database
from GSN import database
# Mail
from GSN.mail import mail

mod = Blueprint('registration', __name__, template_folder='templates')



# Handling post request
@mod.route("/registration", methods = ["GET", "POST"])
def registration():
    if request.method == 'POST':
        # Take info from form on registration page
        login = request.form.get("login")
        password = request.form.get("password")
        email = request.form.get("email")
        # Selecting from database user with given login for checking
        used = database.Users.query.filter_by(login=login).first()
        # Checking if email is unique
        if used is not None:
            error = ' Login is already used '
            return render_template("Registration.html", error=error,plogin=login,pemail=email)
        # Selecting from database login for checking
        used = database.Users.query.filter_by(email=email).first()
        # Checking if email and login are unique
        if used is not None:
            error = ' Email is already used '
            return render_template("Registration.html", error=error,plogin=login,pemail=email)
        # Insert into database
        activation_link = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
        user = database.Users(login=login,email=email,password=generate_password_hash(password), activation_link = activation_link)
        database.db.session.add(user)
        database.db.session.commit()
        # Send massage 
        send_email('Hello', 'geosocnetwork@gmail.com',[email], render_template("msg.html", user = 'User',login=login,link=activation_link))
        return render_template("emailConfirmation.html")
    elif request.method == 'GET':
        if g.user:
            return redirect(url_for('map.map'))
    return render_template("Registration.html")



def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.html = html_body
    mail.send(msg)