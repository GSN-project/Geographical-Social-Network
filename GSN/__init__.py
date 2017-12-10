from flask import Flask, g, session,request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import random
import string
from flask_uploads import configure_uploads
# Database
from GSN import database
# Mail
from GSN import mail
# Blueprints
from GSN.application import application
from GSN.login import login
from GSN.registration import registration
from GSN.logout import logout
from GSN.profile import profile
from GSN.map import map
from GSN.logout import logout
from GSN.profile import profile
from GSN.friends import friends
from GSN.user import user
from .config import photos



def create_app(config = None):
	# App
	app = Flask(__name__)
	app.config.from_object(__name__)
	# Database:
	#  - Heroku
	#    If you youse it, all objects "User" have to be "Users"
	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://r01bghd36z2ld54q:i0kfbhifxcnyrf0r@x3ztd854gaa7on6s.cbetxkdyhwsb.us-east-1.rds.amazonaws.com/lreehpo3s6bwktzb'
	#  - freemysqlhosting.net
	#    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sql11202817:VjJvatfyw2@sql11.freemysqlhosting.net/sql11202817'
	#  - local (Slavik)
	#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:aist2371@localhost/gsn'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
	database.db.init_app(app)
	# Mail
	app.config['MAIL_SERVER']='smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USERNAME'] = 'geosocnetwork@gmail.com'
	app.config['MAIL_PASSWORD'] = 'GeographicalSocialNetwork'
	app.config['MAIL_USE_TLS'] = False
	app.config['MAIL_USE_SSL'] = True
	mail.mail.init_app(app)

	#photos = UploadSet('photos', IMAGES)
	
	app.config['UPLOADED_PHOTOS_DEST'] = 'GSN/static/img/user'
	
	# Blueprints
	app.register_blueprint(application.mod)
	app.register_blueprint(login.mod)
	app.register_blueprint(registration.mod)
	app.register_blueprint(map.mod)
	app.register_blueprint(logout.mod)
	app.register_blueprint(profile.mod)
	app.register_blueprint(friends.mod)
	app.register_blueprint(user.mod)
	# Session
	app.secret_key = os.urandom(24)
	
	
	configure_uploads(app, photos)

# This route takes place before any request
	@app.before_request
	def before_request():
		g.user = None
		if 'user_id' in session:
			g.user = database.Users.query.filter_by(user_id=session['user_id']).first()
			g.user_info = database.UsersInfo.query.filter_by(user_id=session['user_id']).first()
		
	
	return app

	