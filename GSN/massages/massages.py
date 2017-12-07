import os
import smtplib
from flask_mail import Mail, Message
from flask import Flask, render_template, request, g, redirect, session, url_for, json, jsonify, Blueprint
from werkzeug import check_password_hash, generate_password_hash
import random
import string
from flask_uploads import UploadSet, configure_uploads, IMAGES
# Database
from GSN import database
# Mail
from GSN.mail import mail

mod = Blueprint('massages', __name__, template_folder='templates')

@mod.route("/massages", methods = ["GET", "POST"])
def massages:
	if request.method == 'GET':
		if not g.user:
			return redirect(url_for('registration.registration'))
		else:
			# TODO
			

			return render_template()
	else:

@mod.route("/get_chats", methods = ["GET"])
def get_chats():
	chats = database.Chat.query.filter_by(member = g.user.user_id).first()
	jsonrespond =[]
	for chat in chats:
		jsonrespond.append({'chat_name': chat.chat_name,'chat_id': chat.chat_id})
	return json.dumps(jsonrespond)

@mod.route("/get_massages", methods = ["GET"])
def get_massages():
	chat_id = request.form.get("chat_id")
	massages = database.Massages.query.filter_by(chat_id = chat_id).all()
	jsonrespond =[]
	members = [[g.user.user_id, g.user.name, g.user_info.surname]]  
	for massage in massages:
		if massages.author_id != members[0][0]:
			second_member = database.UsersInfo.query.filter_by(user_id = massage.author_id).first()
			members.append([second_member.user_id, second_member.name, second_member.surname])
			author_fullname = second_member.name + second_member.surname
		elif massages.author_id == members[0][0]:
			author_fullname = members[0][1] + members[0][2]
		else:
			author_fullname = members[1][1] + members[1][2]
		jsonrespond.append({'author_fullname': author_fullname, 'text': massage.text, 'time': massage.date, 'massage_id' : massage.massage_id})
	return json.dumps(jsonrespond)




@mod.route("/send", methods = ["POST"])
def send_massage:
	text = request.form.get("text")
	# TODO : nice definition of chat id
	chat_id = request.form.get("chat_id")
	massage = database.Massages(author_id = g.user.user_id, chat_id = chat_id, text = text)
	database.db.session.add(massage)
    database.db.session.commit()
