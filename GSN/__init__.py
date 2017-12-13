from flask import Flask, g, session,request,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
import random
import string
from flask_uploads import configure_uploads
from flask_migrate import Migrate
# Database
from GSN import database
from GSN.database import db
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
from GSN.message import message
from .config import photos



def create_app(config = None):
	# App
	app = Flask(__name__)
	app.config.from_object(__name__)
	# Database:
	#  - Heroku

	app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://r01bghd36z2ld54q:i0kfbhifxcnyrf0r@x3ztd854gaa7on6s.cbetxkdyhwsb.us-east-1.rds.amazonaws.com/lreehpo3s6bwktzb'
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	database.db.init_app(app)
	migrate = Migrate(app, db)

	# Mail
	app.config['MAIL_SERVER']='smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USERNAME'] =    'geographicalsocialnetwork@gmail.com'
	app.config['MAIL_PASSWORD'] = 'Geosocnetwork'
	app.config['MAIL_USE_TLS'] = False
	app.config['MAIL_USE_SSL'] = True
	mail.mail.init_app(app)

	#photos = UploadSet('photos', IMAGES)
	app.config['UPLOAD_FOLDER'] = 'GSN\\static\\img'
	app.config['UPLOADED_PHOTOS_DEST'] = 'GSN/static/img/user'
	app.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024
	
	# Blueprints
	app.register_blueprint(application.mod)
	app.register_blueprint(login.mod)
	app.register_blueprint(registration.mod)
	app.register_blueprint(map.mod)
	app.register_blueprint(logout.mod)
	app.register_blueprint(profile.mod)
	app.register_blueprint(friends.mod)
	app.register_blueprint(user.mod)
	app.register_blueprint(message.mod)
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

	
