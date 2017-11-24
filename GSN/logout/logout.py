import os
import smtplib
from flask_mail import Mail, Message
from flask import Flask, render_template, request, g, redirect, session, url_for,json,jsonify, Blueprint
from flask_mysqldb import MySQL
from werkzeug import check_password_hash, generate_password_hash
import random
import string
from flask_uploads import UploadSet, configure_uploads, IMAGES
from MySQLdb.cursors import DictCursor
# Database
from GSN import database

mod = Blueprint('logout', __name__)

@mod.route("/logout")
def logout():
    g.user = None;
    session.pop('user_id', None);
    return render_template('login.html', error='You were logouted') 