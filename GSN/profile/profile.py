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

mod = Blueprint('profile', __name__, template_folder='templates')

@mod.route("/myprofile", methods = ['GET', 'POST'])
def myprofile():
    if request.method == 'POST':
        if g.user is None:
            return redirect(url_for('login.login'))
        user = database.Users.query.filter_by(user_id=g.user.user_id).first()
        user_info = database.UsersInfo.query.filter_by(user_id=g.user.user_id).first()
        if user_info.ava_ref is not None:
            ref_ava = mod.config['UPLOADED_PHOTOS_DEST'] + '/' + user_info.ava_ref
        else:
            ref_ava = 'static/img/avatar.png'
        return render_template('MyProfileSettings.html', ava=ref_ava, name=user.name, surname=user_info.surname, email=user.email, country=user_info.country, city=user_info.city,date=user_info.date,sex=user_info.sex,telephone=user_info.telephone, about=user_info.about)
    else:
        if g.user is None:
            return redirect(url_for('login.login'))

        user = database.Users.query.filter_by(user_id=g.user.user_id).first()
        user_info = database.UsersInfo.query.filter_by(user_id=g.user.user_id).first()
        if user_info is None:
            user_info = database.UsersInfo(user_id=g.user.user_id)
            database.db.session.add(user_info)
   

        fname = request.form.get("name")
        user.name = fname

        fsurname = request.form.get("surname")
        user_info.surname = fsurname
          
        femail = request.form.get("email")
        user.email = femail
          
        fsex = request.form.get("sex")
        user_info.sex = fsex
          
        fcountry = request.form.get("country")
        user_info.country = fcountry

        fcity = request.form.get("city")
        user_info.city = fcity

        fdate = request.form.get("date")
        user_info.date = fdate

        ftelephone = request.form.get("telephone")
        user_info.telephone = ftelephone

        fabout = request.form.get("about")
        user_info.about = fabout

        database.db.session.commit()
        return render_template('MyProfileSettings.html', ava=user_info.ava_ref, name=user.name, surname=user_info.surname, email=user.email, country=user_info.country, city=user_info.city,date=user_info.date,sex=user_info.sex,telephone=user_info.telephone, about=user_info.about)


# @mod.route('/upload', methods=['POST'])
# def upload():
#    if 'photo' in request.files:
#        cur_id = g.user['user_id']
#        cur = mysql.connection.cursor()
       
#        #if user already has an avatar - delete
#        if (g.user['ava_ref'] is not None):
#            os.remove(mod.config['UPLOADED_PHOTOS_DEST'] + '/' + g.user['ava_ref'])

#        fname = photos.save(request.files['photo'])
#        #appending random prefix to name of the file to prevent name collision
#        rand_prefix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
#        os.rename(mod.config['UPLOADED_PHOTOS_DEST'] + '/' + fname, 
#                  mod.config['UPLOADED_PHOTOS_DEST'] + '/' + rand_prefix + fname)
       
#        cur.execute('''UPDATE users SET ava_ref = %s WHERE user_id = %s''', (rand_prefix + fname, cur_id))
#        mysql.connection.commit()
#    return redirect(url_for('myprofget'))

