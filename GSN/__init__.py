from flask import Flask, g, session
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_sqlalchemy import SQLAlchemy
import os
# Database
from GSN import database
# Mail
from GSN import mail
# Blueprints
from GSN.application.application import mod
from GSN.login.login import mod
from GSN.registration.registration import mod
from GSN.logout.logout import mod
from GSN.profile.profile import mod
from GSN.map.map import mod
from GSN.logout.logout import mod
from GSN.profile.profile import mod


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
	# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:aist2371@localhost/gsn'
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
	# Blueprints
	app.register_blueprint(application.application.mod)
	app.register_blueprint(login.login.mod)
	app.register_blueprint(registration.registration.mod)
	app.register_blueprint(map.map.mod)
	app.register_blueprint(logout.logout.mod)
	app.register_blueprint(profile.profile.mod)
	# Session
	app.secret_key = os.urandom(24)
	# Photos
	photos = UploadSet('photos', IMAGES)
	# Uplodes
	app.config['UPLOADED_PHOTOS_DEST'] = 'static/img/user'
	configure_uploads(app, photos)

	# This route takes place before any request
	@app.before_request
	def before_request():
	    g.user = None
	    if 'user_id' in session:
	        g.user = database.Users.query.filter_by(user_id=session['user_id']).first()
	        #g.user_info = database.UsersInfo.query.filter_by(user_id=session['user_id']).first()

	@app.route('/upload', methods=['POST'])
	def upload():
		if 'photo' in request.files:
			cur = mysql.connection.cursor()
			#if user already has an avatar - delete

			if g.user_info.ava_ref is not None:
				os.remove(mod.config['UPLOADED_PHOTOS_DEST'] + '/' + g.user.user_info)
			fname = photos.save(request.files['photo'])

			#appending random prefix to name of the file to prevent name collision
			rand_prefix = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(15))
			os.rename(app.config['UPLOADED_PHOTOS_DEST'] + '/' + fname, app.config['UPLOADED_PHOTOS_DEST'] + '/' + rand_prefix + fname) 
			g.user_info.ava_ref = rand_prefix + fname
			database.db.session.commit()
		return redirect(url_for('profile.myprofget'))
	return app
