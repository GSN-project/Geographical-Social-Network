import os
import smtplib
import datetime
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
    locs= database.Posts.query.filter((database.Posts.privacy==2) | (database.Posts.author_id==g.user.user_id)).all()
    
    jsonrespond =[]
    for loc in locs:
        jsonrespond.append({'id':loc.post_id, 'author':loc.author.login,'author_id': loc.author_id,
                                'title': loc.title,'lat': loc.lat, 'lng' : loc.lng, 'description': loc.description}) #,'dateTime':loc.dateTime
    return json.dumps(jsonrespond)


@mod.route("/add_pin/", methods = ["POST"])
def add_pin(): 
    lat =  request.form.get("c1")
    lng = request.form.get("c2")
    title=request.form.get("title")
    priv=request.form.get("priv")
    dsp=request.form.get("dsp")

    print(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
          
    pin = database.Posts(author_id=g.user.user_id, title=title, lat=lat, lng=lng,
                         privacy=priv, description=dsp)#dateTime=datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    database.db.session.add(pin)
    database.db.session.commit()
    return json.dumps('')

#comments processing functions
#
comments=[]
#

@mod.route("/get_comments/", methods = ["GET"])
def get_comments():
    arg=request.args.get("id")
    #
    #for i in range (2):
    #    comments.append({'author':"someAuthor",'id':arg,'text':("comment "+str(i)+" for pin id:"+str(arg)),'likes':0,'time':"11:11"})
    #
    comments= database.Comments.query.filter((database.Comments.post_id==arg) & (database.Comments.photo_id==None)).all()
    jsonrespond =[]
    for loc in coments:
        jsonrespond..append({'author':loc.author.login,'id':loc.comment_id,'text':loc.text,'likes':loc.likes,'time':loc.date})
    return json.dumps(comments)


@mod.route("/add_pin_comment/", methods = ["POST"])
def add_pin_comment():
    text=request.form.get("text")
    postId=request.form.get("id")
    #
    backComment={'author':g.user.login,'id':pinId,'text':text,'likes':0}
    #comments.append(comment)
    
    comment = database.Comments(author_id=g.user.user_id, post_id=postId,photo_id=None,
                        text=text,likes=0) #no photo id
    database.db.session.add(comment)
    database.db.session.commit()
    return json.dumps(backComment)


    
