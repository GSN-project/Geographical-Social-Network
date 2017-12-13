from flask import Flask, render_template, request, g, redirect, session, url_for, json, jsonify, Blueprint
# Database
from GSN import database

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
			# If user has not name or surname, save login
			if second_member.name == None or second_member.surname == None:
				second_member_main_info = database.Users.query.filter_by(user_id = message.author_id).first()
				author_fullname = second_member_main_info.login
			else: 
				author_fullname = second_member.name + second_member.surname
		# if message's author is our user we save his fullname in variable
		elif message.author_id == members[0][0]:
			author_fullname = members[0][1] + " " + members[0][2]
		# if message's author is our second member we save his fullname in variable
		else:
			author_fullname = members[1][1] + " " + members[1][2]

		author=database.UsersInfo.query.filter(database.UsersInfo.user_id==message.author_id).first()
		# Append jsonrespond
		jsonrespond.append({'ava':author.ava_ref, 'author_fullname': author_fullname, 'text': message.text, 'time': message.date, 'message_id' : message.message_id, 'author_id' : message.author_id, 'current_user' : g.user.user_id })


	return json.dumps(jsonrespond)


@mod.route("/send/", methods = ["POST"])
def send_message():
	text = request.form.get("msg")
	chat_id = request.form.get("chat_id")

	# TODO : nice definition of chat id
	chat = database.Chat.query.filter_by(chat_id = chat_id).first()

	#new_chat = database.Chat(first_member_id = g.user.user_id, second_member_id= |id человека на которого подписывается юзер|)
	#database.db.session.add(new_chat)
	#database.db.session.commit()
	#new_message = database.Messages(author_id = |id человека на которого подписывается юзер|, chat_id = new_chat.chat_id, text = "Привет. Давай общаться!", read = False)
	#database.db.session.add(new_message)
	#database.db.session.commit()
	#new_chat.last_message_id = new_message.message_id
	#database.db.session.commit()

	message = database.Messages(author_id = g.user.user_id, chat_id = chat_id, text = text, read = False, date = cur_time())
	database.db.session.add(message)
	database.db.session.commit()

	chat.last_message_id = message.message_id
	database.db.session.commit()

	jsonrespond =[]
	# добавить фото и время
	jsonrespond.append({'name': g.user_info.name + ' ' + g.user_info.surname, 'text': text})
	return json.dumps(jsonrespond)








@mod.route("/delete/<int:message_id>", methods = ["GET"])
def delete_message():
	print(message_id)
	# Find message
	message = database.Messages.query.filter_by(message_id = message_id).first()
	db.session.delete(message)
	database.db.session.commit()


def cur_time():
    now = datetime.datetime.now()
    return ( (('0'+str(now.hour)) if (now.hour<10) else str(now.hour))+':'+(('0'+str(now.minute)) if (now.minute<10) else str(now.minute))+' '+str(now.day)+'/'+str(now.month))


