import os
import smtplib
from flask_mail import Mail, Message
from flask import Flask, render_template, request, g, redirect, session, url_for
from flask_mysqldb import MySQL
from werkzeug import check_password_hash, generate_password_hash
#from flask_session import Session


#COnfigure app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'x3ztd854gaa7on6s.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'r01bghd36z2ld54q'
app.config['MYSQL_PASSWORD'] = 'i0kfbhifxcnyrf0r'
app.config['MYSQL_DB'] = 'lreehpo3s6bwktzb'
mysql = MySQL(app)

#mail configs
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'geosocnetwork@gmail.com'
app.config['MAIL_PASSWORD'] = 'GeographicalSocialNetwork'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#Config cookies
app.secret_key = os.urandom(24)



@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM users WHERE user_id = %s''', [session['user_id']])
        g.user = make_dicts(cur)

#Mapping on localhost
@app.route("/")
def index():
    if g.user:
        return render_template("Map.html")
    else:
        return render_template("Registration.html")

# Handling post request
@app.route("/registration", methods = ["POST"])
def registration():
    name = request.form.get("name")
    login = request.form.get("login")
    password = request.form.get("password")
    email = request.form.get("email")

    # Checking if email and login are unique
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM users WHERE login = %s''', [login])
    used = cur.fetchall()
    if used is not ():
        error = ' Login is already used '
        return render_template("Registration.html", error=error)
    cur.execute('''SELECT * FROM users WHERE email = %s''', [email])
    used = cur.fetchall()
    if used is not ():
        error = ' Email is already used '
        return render_template("Registration.html", error=error)
    
    # Insert into database
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO users (name, login, email, password) VALUES (%s , %s , %s , %s)''', (name, login, email, generate_password_hash(password) ))
    mysql.connection.commit()
    
    # Send massage 
    send_email('Hello', 'geosocnetwork@gmail.com',[email], render_template("msg.html", user = name))
    return render_template("success.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for('showAll'))
    error = None
    if request.method == 'POST':
        login = request.form.get("login")
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM users WHERE login = %s''', [login])
        user = make_dicts(cur)
        print(user)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user["password"], request.form.get("password")):
            error = 'Invalid password'
        else :
            error = 'You were logged in'
            session['user_id'] = user['user_id']
    return render_template('login.html', error=error) 


@app.route("/all", methods = ["GET"])
def showAll():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM users''')
    users = cur.fetchall()
    toShow = ""
    for user in users:
        toShow += str(user) + "<br>"
    return toShow

# There is helper function, which takes as cursor from request
# and return dictionary. Keys are column's name
def make_dicts(cursor):
    row = cursor.fetchall()
    if row is ():
        return None
    else:
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row[0]))

def send_email(subject, sender, recipients, html_body):
    msg = Message(subject, sender = sender, recipients = recipients)
    msg.html = html_body
    mail.send(msg)


#if __name__ == '__main__':
   # app.run(debug=True)

if __name__ == '__main__':
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
