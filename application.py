import smtplib
from flask import Flask, render_template, request, g, redirect, session, url_for
from flask_mysqldb import MySQL
from werkzeug import check_password_hash, generate_password_hash
#from flask_session import Session

# For session
#SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

#COnfigure app
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'sql11.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql11202817'
app.config['MYSQL_PASSWORD'] = 'VjJvatfyw2'
app.config['MYSQL_DB'] = 'sql11202817'
mysql = MySQL(app)

#Config cookies
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM users WHERE user_id = %s''', (session['user_id']))
        g.user = cur.fetchall()

#Mapping on localhost
@app.route("/")
def index():
    return render_template("Registration.html")

# Handling post request
@app.route("/registration", methods = ["POST"])
def registration():
    name = request.form.get("name")
    login = request.form.get("login")
    password = request.form.get("password")
    email = request.form.get("email")

    # Checking if email and login is unique
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
    cur.execute('''INSERT INTO users (name, login, email, password) VALUES (%s , %s , %s , %s)''', (name, login, email, generate_password_hash(password) ))
    mysql.connection.commit()
#Send massage (Error)
#    massage = "You are registrated!"
#    server = smtplib.SMTP("smtp.gmail.com", 587)
#    server.starttls()
#    server.login("jharvard@cs50.net", os.getenv("PASSWORD"))
#    server.sendmail("jharvard@cs50.net", email, massage)
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
        user = cur.fetchall()
        if user is ():
            error = 'Invalid username'
        elif not check_password_hash(user[0][4], request.form.get("password")):
            error = 'Invalid password'
        else :
            error = 'You were logged in'
#            session['user_id'] = user[0][0]
    return render_template('login.html', error=error) 


@app.route("/all", methods = ["GET"])
def showAll():
#    print(session['user_id'])
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM users''')
    users = cur.fetchall()
    toShow = ""
    for user in users:
        toShow += str(user) + "<br>"
    return toShow

if __name__ == '__main__':
    app.run(debug=True)
