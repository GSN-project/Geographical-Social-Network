import os
import smtplib
import datetime
from flask import current_app as app
from flask_mail import Mail, Message
from flask import Flask, render_template, request, g, redirect, session, url_for,json,jsonify, Blueprint
from flask_mysqldb import MySQL
from werkzeug import check_password_hash, generate_password_hash
import random
import string
from flask_uploads import UploadSet, configure_uploads, IMAGES
from MySQLdb.cursors import DictCursor
from werkzeug.utils import secure_filename
from flask import send_from_directory
from time import gmtime, strftime
# Database
from GSN import database

mod = Blueprint('map', __name__, template_folder='templates')

POST_COUNT=0
end=0
STATIC_FOLDER="../../static/img/" #note: may change on heroku

@mod.route('/map')
def map():
    if g.user:
        return render_template("Map.html")
    else: 
        return render_template("Registration.html")


def cur_time():
    return strftime("%m-%d %H:%M", gmtime())

@mod.route("/get_locations/", methods = ["GET"])
def get_locations():
    locs= database.Posts.query.filter((database.Posts.privacy==2) | (database.Posts.author_id==g.user.user_id)).all()
    
    jsonrespond =[]
    for loc in locs:
        jsonrespond.append({'id':loc.post_id,'author_id': loc.author_id,
                                'title': loc.title,'lat': loc.lat, 'lng' : loc.lng, 'description': loc.description,'priv':loc.privacy}) #,'dateTime':loc.dateTime
    return json.dumps(jsonrespond)


@mod.route("/focus_pin/", methods = ["POST"])
def focus_pin():
    id=request.form.get("id")
    global end
    global POST_COUNT
    POST_COUNT=database.Photos.query.filter(database.Photos.post_id==id).count()
    end=0
    return json.dumps({'c':POST_COUNT})


@mod.route("/update_private/", methods = ["POST"])
def update_private():
    Id=int(request.form.get("id"))
    lat =  request.form.get("c1")
    lng = request.form.get("c2")
    mark=database.Posts.query.filter(database.Posts.post_id==Id).all()
    mark[0].lat=lat
    mark[0].lng=lng
    database.db.session.commit()
    return ''''''

@mod.route("/delete_pin/", methods = ["POST"])
def delete_pin():
    Id=int(request.form.get("id"))
    print(Id)
    mark=database.Posts.query.filter(database.Posts.post_id==Id).all()
    database.db.session.delete(mark[0])
    database.db.session.commit()
    return ''''''

    
@mod.route("/add_pin/", methods = ["POST"])
def add_pin(): 
    lat =  request.form.get("c1")
    lng = request.form.get("c2")
    title=request.form.get("title")
    priv=request.form.get("priv")
    dsp=request.form.get("dsp")
          
    pin = database.Posts(author_id=g.user.user_id, title=title, lat=lat, lng=lng,
                         privacy=priv, description=dsp) #dateTime=cur_time()
    database.db.session.add(pin)
    database.db.session.commit()
    return json.dumps('')


#comments processing functions
comments=[]

@mod.route("/get_comments/", methods = ["GET"])
def get_comments():
    arg=request.args.get("id")
    typ=request.args.get("type")
    if typ == "0":
        comments= database.Comments.query.filter((database.Comments.post_id==arg) & (database.Comments.photo_id==None)).all()
    else:
        comments= database.Comments.query.filter(database.Comments.photo_id==arg).all()
    jsonrespond =[]
    for loc in comments:
        jsonrespond.append({'author':loc.author.login,'id':loc.comment_id,'text':loc.text,'likes':loc.likes,'date':loc.date})
    return json.dumps(jsonrespond)  



@mod.route("/add_pin_comment/", methods = ["POST"])
def add_pin_comment():
    text=request.form.get("text")
    Id=request.form.get("id")
    typ=request.form.get("type")
    backComment={'author':g.user.login,'id':Id,'text':text,'likes':0}#,'ava':"../../static/img/user"+str(g.user.ava_ref)
    if typ=="0":
        comment = database.Comments(author_id=g.user.user_id, post_id=Id,photo_id=None,
                        text=text,likes=0,date=cur_time()) #no photo id
    else:
         comment = database.Comments(author_id=g.user.user_id, post_id=None,photo_id=Id,
                        text=text,likes=0,date=cur_time())
    database.db.session.add(comment)
    database.db.session.commit()
    backComment={'author':g.user.login,'id':comment.comment_id,'text':text,'likes':0,'date':cur_time()}
    return json.dumps(backComment)



@mod.route('/like_comment/', methods=['POST'])
def like_comment():
    #TODO: remember who likes, stop multiple
    c_id=request.form.get('id')
    comment=database.Comments.query.filter(database.Comments.comment_id==c_id).all()
    comment=comment[0]
    comment.likes=comment.likes+1
    database.db.session.commit()
    return json.dumps({'l':comment.likes})
    




#photos uploading and post processing

ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@mod.route('/new_post/', methods=['POST','GET'])                
def new_post():
        file = None
        isFile=request.form.get("type")
        if isFile is '1':
            file = request.files['file']
        marker_id=request.form.get("marker_id")
        text=request.form.get("text")
        title=request.form.get("title")
        post = database.Photos(author_id=g.user.user_id, post_id=marker_id,
                        text=text,likes=0,title=title,date=cur_time())

        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                rand_prefix = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(15))
                os.rename(app.config['UPLOAD_FOLDER']+"\\"+filename, app.config['UPLOAD_FOLDER'] +"\\"+ rand_prefix + filename) 
                new_name=rand_prefix+filename
                post.photo_ref=new_name
            else:
                return "Extension not allowed" #error page

        database.db.session.add(post)
        database.db.session.commit()
        return "OK"

    

@mod.route('/uploads/<filename>/')
def send_file(filename):
    return redirect(url_for('static', filename='img/'+filename))
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


#new
@mod.route('/like_photo/', methods=['POST'])
def like_photo():
    photo_id=request.form.get("id")
    photo=database.Photos.query.filter(database.Photos.photo_id==photo_id).all()
    photo=photo[0]
    photo.likes=photo.likes+1
    database.db.session.commit()
    return json.dumps({'l':photo.likes})
    #TODO: remember who likes, stop multiple


#new
@mod.route('/get_post/',methods =['GET','POST'])
def get_post():
    global end
    id=request.form.get("id") 
    lim=10 #rel to count in Map.html, need sync on change
    begin=int(request.form.get("begin"))
    start=POST_COUNT-begin
    if begin==lim:
        end=0
    jsonrespond=[]
    
    if start <=0 and end==0:
        lim=lim-(-start%10)
        start=0
        end=1
    elif start <= 0:
        return json.dumps(jsonrespond)
    
    
    if POST_COUNT<10:
        photos=database.Photos.query.filter(database.Photos.post_id==id).all()
    else: 
        photos=database.Photos.query.filter(database.Photos.post_id==id).limit(lim).offset(start).all()
    jsonrespond=[]   
    for i in range (len(photos)-1,-1,-1):
        loc=photos[i]
        if loc.photo_ref is not None:
            jsonrespond.append({'title':loc.title,'author':loc.author.login,'id':loc.photo_id,'text':loc.text,'likes':loc.likes,'date':loc.date,
                                  'photo_ref':STATIC_FOLDER+str(loc.photo_ref)})
        else:
            jsonrespond.append({'title':loc.title,'author':loc.author.login,'id':loc.photo_id,'text':loc.text,'likes':loc.likes,'date':loc.date,
                            'photo_ref':"No photo"})
    lim=10
    return json.dumps(jsonrespond)
    


           

