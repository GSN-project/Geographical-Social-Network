from flask import Flask, render_template, request, g, redirect, session, url_for, json, jsonify, Blueprint
from flask_socketio import SocketIO, send
# Database
from GSN import database
# Messages
from .. import socketio

mod = Blueprint('message', __name__, template_folder='templates')

@mod.route("/message")
def messages():
	if not g.user:
		return redirect(url_for('registration.registration'))
	else:
		return render_template('message.html')

@mod.route("/get_chats/", methods = ["GET"])
def get_chats():
	# Take all chats where user participate 
	chats = database.Chat.query.filter_by(first_member_id = g.user.user_id).all()
	# Create json respond
	jsonrespond =[]
	# Check whether chats iterable or not
	if iter(chats):
		for chat in chats:
			# Find second member's name and surname
			second_member = database.UsersInfo.query.filter_by(user_id = chat.second_member_id).first()
			# Find last chat's message 
			last_message = database.Messages.query.filter_by(message_id = chat.last_message_id).first()
			# Insert info into json
			jsonrespond.append({'member': second_member.name + ' ' + second_member.surname, 'chat_id': chat.chat_id, 'last_message_body': last_message.text, 'read': last_message.read})
	else:
		# Find second member's name and surname
		second_member = database.UsersInfo.query.filter_by(user_id = chats.second_member_id).first()
		# Find last chat's message 
		last_message = database.Messages.query.filter_by(message_id = chats.last_message_id).first()
		jsonrespond.append({'member': second_member.name + ' ' + second_member.surname, 'chat_id': chat.chat_id, 'last_message_body': last_message.text, 'read': last_message.read})
	print(jsonrespond)
	return json.dumps(jsonrespond)


@mod.route("/get_messages/<int:chat_id>", methods = ["GET"])
def get_messages(chat_id):
	# Get chat id from user
	#chat_id = request.form.get("chat_id")
	# Select all messages from this chat
	# TODO: Maybe we should take only 10 which we need
	messages = database.Messages.query.filter_by(chat_id = chat_id).all()
	# Create json respond
	jsonrespond =[]
	# Create array with information about chat's members
	# TODO: Maybe we should use dict or other structure to save this information
	members = [[g.user.user_id, g.user_info.name, g.user_info.surname]]  
	for message in messages:
		# if message's author is't our existing member which we add to array,
		# TODO: Change a way we interact with array to use chat with more than 2 members
		if message.author_id != members[0][0]:
			# Select information about our new member
			second_member = database.UsersInfo.query.filter_by(user_id = message.author_id).first()
			# Add information to array
			members.append([second_member.user_id, second_member.name, second_member.surname])
			# Create useful variable to save author's fullname
			author_fullname = second_member.name + second_member.surname
		# if message's author is our user we save his fullname in variable
		elif message.author_id == members[0][0]:
			author_fullname = members[0][1] + members[0][2]
		# if message's author is our second member we save his fullname in variable
		else:
			author_fullname = members[1][1] + members[1][2]
		# Append jsonrespond
		jsonrespond.append({'author_fullname': author_fullname, 'text': message.text, 'time': message.date, 'massage_id' : message.message_id})

	print(jsonrespond)

	return json.dumps(jsonrespond)


@mod.route("/send/", methods = ["POST"])
def send_message():
	text = request.form.get("text")
	chat_id = request.form.get("chat_id")
	# TODO : nice definition of chat id
	massage = database.Messages(author_id = g.user.user_id, chat_id = chat_id, text = text, read = False)
	database.db.session.add(massage)
	database.db.session.commit()


@mod.route("/edit", methods = ["POST"])
def edit_message():
	# TODO
	pass

@mod.route("/delete", methods = ["POST"])
def delete_message():
	# TODO
	pass

@mod.route("/delete_story", methods = ["POST"])
def delete_story():
	# TODO
	pass	


@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	# Broadcast - отправляет сообщения всем, кто подключён к чату
	# False если  только отправителю и тебе
	send(msg, broadcast=True)


# 1. Грузится страница и получает список чатов, к которому подключен пользователь. 
# 2. Пользователь нажимает на нужный чат и запрашивает чат 
#
#
#
#
#
#