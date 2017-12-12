from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import datetime
#To set database up
#from flask import Flask
#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:aist2371@localhost/gsn'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =  False
#db = SQLAlchemy(app)
db = SQLAlchemy()

# Here should be defined all models
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    timestamp = db.Column(db.String(50), default=datetime.datetime.utcnow)

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20))
    email = db.Column(db.String(50))
    password = db.Column(db.String(160))
    activation_link = db.Column(db.String(20))
    
    follows = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=db.backref('followers', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], backref=db.backref('followed', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    
    def userpic(self):
        usInfo = self.user_info.first()
        if usInfo.ava_ref is not None:
            ref_ava = '/static/img/user' + '/' + usInfo.ava_ref
        else:
            ref_ava = '/static/img/avatar.png'

        #print ('Avatar reference: ', ref_ava)
        return ref_ava
    
    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower_id=self.user_id, followed_id=user.user_id)
            db.session.add(f)
    
    def unfollow(self, user):
        f = self.follows.filter_by(followed_id=user.user_id).first()
        if f:
            db.session.delete(f)
    
    #this function takes user as Follow or User object from different places in code
    def is_following(self, user):
        if isinstance(user, Users):
            return self.follows.filter_by(followed_id=user.user_id).first() is not None
        else: #if is instance of Follow
            return user in self.follows.all()
        #print ('User', user, 'follows.all', self.follows.all())
        #return user in self.follows.all()

class UsersInfo(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(30))
    sex = db.Column(db.String(6))
    country = db.Column(db.String(30))
    city= db.Column(db.String(30))
    date = db.Column(db.Date)
    telephone = db.Column(db.String(15))
    about = db.Column(db.String(200))
    ava_ref = db.Column(db.String(100))
    user = db.relationship('Users', backref=db.backref('user_info', lazy='dynamic'))

class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    title = db.Column(db.String(150))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    privacy = db.Column(db.Integer)
    description = db.Column(db.Text)
    date = db.Column(db.String(50), default=datetime.datetime.utcnow)

    author = db.relationship('Users', backref=db.backref('posts'))


class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.photo_id'))
    text = db.Column(db.Text) 
    date = db.Column(db.String(50), default=datetime.datetime.utcnow)
    likes = db.Column(db.Integer)
    author = db.relationship('Users', backref=db.backref('Comments', lazy=True))

class Photos(db.Model):
    photo_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    text = db.Column(db.Text) 
    date = db.Column(db.String(50), default=datetime.datetime.utcnow)
    photo_ref = db.Column(db.String(100))
    likes = db.Column(db.Integer)
    title = db.Column(db.String(150))
    author = db.relationship('Users', backref=db.backref('photos'))

class Massages(db.Model):
    massage_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))    
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.chat_id'))
    text = db.Column(db.Text) 
    date = db.Column(db.String(50), default=datetime.datetime.utcnow)
    author = db.relationship('Users', backref=db.backref('Massages', lazy=True))

class Chat(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    member = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    chat_name = db.Column(db.String(150))
    memb = db.relationship('Users', backref=db.backref('Chat', lazy=True))

class Likes(db.Model):
    comment_id=db.Column(db.Integer, db.ForeignKey('comments.comment_id'), primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
class LikesPhoto(db.Model):
    photo_id=db.Column(db.Integer, db.ForeignKey('photos.photo_id'), primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)


    
