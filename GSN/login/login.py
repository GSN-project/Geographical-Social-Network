import os
import smtplib
from flask_mail import Mail, Message
from flask import Flask, render_template, request, g, redirect, session, url_for, Blueprint
from flask_mysqldb import MySQL
from werkzeug import check_password_hash, generate_password_hash
import random
import string
from flask_uploads import UploadSet, configure_uploads, IMAGES
# Database
from GSN import database

mod = Blueprint('login', __name__, template_folder='templates')

@mod.route("/login", methods = ["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for('map.map'))
    error = None
    congrads = None
    if request.method == 'POST':
        login = request.form.get("login")
        user = database.Users.query.filter_by(login=login).first()
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user.password, request.form.get("password")):
            error = 'Invalid password'
        elif not user.activation_link == None:
            error='Unactivated profile'
        else :
            error = 'You were logged in. You will be redirected'
            congrads = True
            session['user_id'] = user.user_id
    return render_template('login.html', error=error, congrads=congrads)



@mod.route("/activate/")
def activation():
    login = request.args.get('username')
    link= request.args.get('link')

    user = database.Users.query.filter_by(login=login, activation_link = link).first()

    error = None
    if user is None:
        error = 'Invalid activation link'
    else :
        error = 'You were logged in'
        session['user_id'] = user.user_id
        cur_id = session['user_id']
        user.activation_link = None
        database.db.session.commit()
        # Create info about user
        user_info = database.UsersInfo(user_id=cur_id, surname=None, sex= None, country=None, city=None, date= None, telephone = None, about = None)
        database.db.session.add(user_info)
        database.db.session.commit()
        return redirect(url_for('profile.myprofget'))
    return render_template('login.html', error=error) 


