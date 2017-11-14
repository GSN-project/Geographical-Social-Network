import os
import smtplib
from flask_mail import Mail, Message
from flask import Flask, render_template, request, g, redirect, session, url_for
from flask_mysqldb import MySQL
from werkzeug import check_password_hash, generate_password_hash
import random
import string
from flask_uploads import UploadSet, configure_uploads, IMAGES
#from flask_session import Session

#COnfigure app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'x3ztd854gaa7on6s.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'r01bghd36z2ld54q'
app.config['MYSQL_PASSWORD'] = 'i0kfbhifxcnyrf0r'
app.config['MYSQL_DB'] = 'lreehpo3s6bwktzb'

#app.config['MYSQL_HOST'] = 'sql11.freemysqlhosting.net'
#app.config['MYSQL_USER'] = 'sql11202817'
#app.config['MYSQL_PASSWORD'] = 'VjJvatfyw2'
#app.config['MYSQL_DB'] = 'sql11202817'
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

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img/user'
configure_uploads(app, photos)



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
        return render_template("Registration.html", error=error,pname=name,plogin=login,pemail=email)
    cur.execute('''SELECT * FROM users WHERE email = %s''', [email])
    used = cur.fetchall()
    if used is not ():
        error = ' Email is already used '
        return render_template("Registration.html", error=error,pname=name,plogin=login,pemail=email)
    
    # Insert into database
    token = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(16))
    cur = mysql.connection.cursor()
    cur.execute('''INSERT INTO users (name, login, email, password,activation_link) VALUES (%s , %s , %s , %s,%s)''', (name, login, email, generate_password_hash(password),token ))
    mysql.connection.commit()
    
    # Send message
    send_email('Hello', 'geosocnetwork@gmail.com',[email], render_template("msg.html", user = name,login=login,link=token))
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
        elif not user["activation_link"] == None:
            error='Unactivated profile'
        else :
            error = 'You were logged in'
            session['user_id'] = user['user_id']
    return render_template('login.html', error=error) 

@app.route("/logout")
def logout():
    g.user = None;
    session.pop('user_id', None);
    return render_template('login.html') 



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

@app.route("/activate/")
def activation():
    login = request.args.get('username')
    link= request.args.get('link')
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM users WHERE login = %s AND activation_link = %s''', (login,link))
    user = make_dicts(cur)
    if user is None:
        error = 'Invalid activation link'
    else :
        error = 'You were logged in'
        session['user_id'] = user['user_id']
        cur_id = session['user_id']
        #cur = mysql.connection.cursor()
        mysql.connection.cursor().execute('''UPDATE users SET activation_link = NULL WHERE login = %s AND activation_link = %s''',(login,link))
        mysql.connection.commit()
    return render_template('login.html', error=error) 

@app.route("/myprofile", methods = ['GET'])
def myprofget():
    if not ('user_id'in session):
        return redirect(url_for('login'))
    if g.user['ava_ref'] is not None:
        ref_ava = app.config['UPLOADED_PHOTOS_DEST'] + '/' + g.user['ava_ref']
    else:
        ref_ava = 'static/img/avatar.png'
    return render_template('MyProfile.html', ava=ref_ava, name=g.user['name'], surname=g.user['surname'], email=g.user['email'], country=g.user['country'], city=g.user['city'],date=g.user['date'],sex=g.user['sex'],telephone=g.user['telephone'],about=g.user['about'])

@app.route("/myprofile", methods = ['POST'])
def myprofpost():
    
    if not ('user_id'in session):
        return redirect(url_for('login'))

    cur_id = g.user['user_id']
    cur = mysql.connection.cursor()

    fname = request.form.get("name")
    cur.execute('''UPDATE users SET name = %s WHERE user_id = %s''', (fname, cur_id))

    fsurname = request.form.get("surname")
    cur.execute('''UPDATE users SET surname = %s WHERE user_id = %s''', (fsurname, cur_id))
           
    femail = request.form.get("email")
    cur.execute('''UPDATE users SET email = %s WHERE user_id = %s''', (femail, cur_id))
           
    fsex = request.form.get("sex")
    cur.execute('''UPDATE users SET sex = %s WHERE user_id = %s''', (fsex, cur_id))
           
    fcountry = request.form.get("country")
    cur.execute('''UPDATE users SET country = %s WHERE user_id = %s''', (fcountry, cur_id))

    fcity = request.form.get("city")
    cur.execute('''UPDATE users SET city = %s WHERE user_id = %s''', (fcity, cur_id))

    fdate = request.form.get("date")
    cur.execute('''UPDATE users SET date = %s WHERE user_id = %s''', (fdate, cur_id))

    ftelephone = request.form.get("telephone")
    cur.execute('''UPDATE users SET telephone = %s WHERE user_id = %s''', (ftelephone, cur_id))

    fabout = request.form.get("about")
    cur.execute('''UPDATE users SET about = %s WHERE user_id = %s''', (fabout, cur_id))

    mysql.connection.commit()
    return redirect(url_for('myprofget'))

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' in request.files:
        cur_id = g.user['user_id']
        cur = mysql.connection.cursor()
        
        #if user already has an avatar - delete
        if (g.user['ava_ref'] is not None):
            os.remove(app.config['UPLOADED_PHOTOS_DEST'] + '/' + g.user['ava_ref'])

        fname = photos.save(request.files['photo'])
        #appending random prefix to name of the file to prevent name collision
        rand_prefix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        os.rename(app.config['UPLOADED_PHOTOS_DEST'] + '/' + fname, 
                  app.config['UPLOADED_PHOTOS_DEST'] + '/' + rand_prefix + fname)
        
        cur.execute('''UPDATE users SET ava_ref = %s WHERE user_id = %s''', (rand_prefix + fname, cur_id))
        mysql.connection.commit()
    return redirect(url_for('myprofget'))

if __name__ == '__main__':
    app.run(debug=True)

#if __name__ == '__main__':
 #   port = int(environ.get('PORT', 5000))
 #   app.run(host='0.0.0.0', port=port)
