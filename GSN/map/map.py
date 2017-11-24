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

mod = Blueprint('map', __name__, template_folder='templates')


@mod.route('/map')
def map():
    if g.user:
        return render_template("Map.html")
    else: 
        return render_template("Registration.html")

@mod.route("/get_locations/", methods = ["GET"])
def get_locations():
#    cur = mysql.connection.cursor()
#    cur.execute('''SELECT * FROM posts WHERE privacy=2''') #OR author_id=g.user['user_id']
#    locs=make_dicts_list(cur)
	locs = database.Posts.query.filter_by(privacy=2).all()
	jsonrespond =[]
	for loc in locs:
		jsonrespond.append({'author_id': loc.author_id,'title': loc.title,'lat': loc.lat, 'lng' : loc.lng, 'description': loc.description})
	return json.dumps(jsonrespond)

@mod.route("/add_pin/", methods = ["POST"])
def add_pin(): 
    cur_id = 1
    lat =  request.form.get("c1")
    lng = request.form.get("c2")
    #locs.append({"lat": lat, "lng": lng,"id":12345})
    title=request.form.get("title")
    priv=request.form.get("priv")
    dsp=request.form.get("dsp") 
    #cur = mysql.connection.cursor()
    #cur.execute('''INSERT INTO posts (author_id, title, lat,lng,privacy,description) VALUES (%s , %s , %s , %s,%s,%s)''', (1,title,lat,lng,priv,dsp))
    #mysql.connection.commit()
    pin = database.Posts(author_id=1, title=title, lat=lat, lng=lng, privacy=priv, description=dsp)
    database.db.session.add(pin)
    database.db.session.commit()
    return json.dumps('')

