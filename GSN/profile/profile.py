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
#
#@mod.route("/myprofile", methods = ['GET'])
#def mypofget():
#    return render_template('MyProfileSetting.html')
#    # TODO
#
#
#@mod.route("/myprofile", methods = ['GET'])
#def myprofget():
#    if not g.user:
#        return redirect(url_for('login.login'))
#
#    #if g.user.ava_ref is not None:
#    #    ref_ava = mod.config['UPLOADED_PHOTOS_DEST'] + '/' + g.user.ava_ref
#    #else:
#    #    ref_ava = 'static/img/avatar.png'
#
#    #user_info = database.UsersInfo.query.filter_by(user_id=g.user.user_id).first()
#    return render_template('MyProfileSetting.html', ava=g.user_info.ava_ref, name=g.user.name, surname=g.user_info.surname, email=g.user.email, 
#    country=g.user_info.country, city=g.user_info.city,date=g.user_info.date,sex=g.user_info.sex,telephone=g.user_info.telephone,about=g.user_info.about)


@mod.route("/myprofile", methods = ['GET', 'POST'])
def myprofpost():
    

    if request.method == 'POST':
        if g.user:
            return redirect(url_for('login.login'))
    
            cur_id = g.user.user_id
            user_info = database.UsersInfo.query.filter_by(user_id=g.user.user_id).first()
    
    #        fname = request.form.get("name")
    #        cur.execute('''UPDATE users SET name = %s WHERE user_id = %s''', (fname, cur_id))
    #       Other table (users)
    #        user_info.name = request.form.get("name")
            fsurname = request.form.get("surname")
    #        cur.execute('''UPDATE users SET surname = %s WHERE user_id = %s''', (fsurname, cur_id))
            user_info.surname = fsurname
            print(fsurname)
            femail = request.form.get("email")
    #        cur.execute('''UPDATE users SET email = %s WHERE user_id = %s''', (femail, cur_id))
            g.user.email = femail
            print(femail)
            fsex = request.form.get("sex")
    #        cur.execute('''UPDATE users SET sex = %s WHERE user_id = %s''', (fsex, cur_id))
            user_info.sex = fsex
            print(fsex)
            fcountry = request.form.get("country")
    #        cur.execute('''UPDATE users SET country = %s WHERE user_id = %s''', (fcountry, cur_id))
            user_info.country = fcountry
            print(fcountry)
            fcity = request.form.get("city")
    #        cur.execute('''UPDATE users SET city = %s WHERE user_id = %s''', (fcity, cur_id))
            user_info.city = fcity
            print(fcity)
            fdate = request.form.get("date")
    #        cur.execute('''UPDATE users SET date = %s WHERE user_id = %s''', (fdate, cur_id))
            user_info.date = fdate
            print(fdate)
            ftelephone = request.form.get("telephone")
    #        cur.execute('''UPDATE users SET telephone = %s WHERE user_id = %s''', (ftelephone, cur_id))
            user_info.telephone = ftelephone
            print(ftelephone)
            fabout = request.form.get("about")
    #        cur.execute('''UPDATE users SET about = %s WHERE user_id = %s''', (fabout, cur_id))
            user_info.about = fabout
            print(fabout)
            database.db.session.commit()
            #TODO Make cole page
        return redirect(url_for('myprofget'))
    else:
        if not g.user:
            return redirect(url_for('login.login'))
        return render_template('MyProfileSetting.html', ava=g.user_info.ava_ref, name=g.user.name, surname=g.user_info.surname, email=g.user.email, 
            country=g.user_info.country, city=g.user_info.city,date=g.user_info.date,sex=g.user_info.sex,telephone=g.user_info.telephone,about=g.user_info.about)