from flask import Blueprint,g,redirect,url_for,render_template,flash
#from flask_sqlalchemy import desc
from GSN import database
from ..config import photos
#not beautiful solution
PHOTOS='/static/img/user'

mod = Blueprint('user', __name__, template_folder='templates')


@mod.route('/user/<user_login>', methods = ['GET', 'POST'])
def user(user_login):
    
    if g.user is None:
        return redirect(url_for('login.login'))
    current_user = database.Users.query.filter_by(user_id=g.user.user_id).first()
    user = database.Users.query.filter_by(login=user_login).first()
    user_info = database.UsersInfo.query.filter_by(user_id=user.user_id).first()
    
    #print('\n\n\n  \n\n\n', user.follows.all())

    ref_ava=user.userpic()
    #if user_info.ava_ref is not None:
     #   ref_ava = '/static/img/user' + '/' + user_info.ava_ref
    #else:
     #   ref_ava = '/static/img/avatar.png'
    #print(ref_ava)
    #YouMightNotNeedBackrefs
    #photos = user.photos.order_by(database.Photos.date.desc()).all()
    #pins = user.posts.order_by(database.Posts.date.desc()).all()
    photos = database.Photos.query.filter_by(author_id=user.user_id).order_by(database.Photos.date.desc())
    pins = database.Posts.query.filter_by(author_id=user.user_id)
    return render_template('Profile.html', ava=ref_ava, name=user_info.name, surname=user_info.surname, country=user_info.country, city=user_info.city,date=user_info.date, photos=photos, pins=pins, user=user, current_user=current_user)

@mod.route('/follow/<user_login>')
def follow(user_login):
    if g.user is None:
        return redirect(url_for('login.login'))
    current_user = database.Users.query.filter_by(user_id=g.user.user_id).first()

    user = database.Users.query.filter_by(login=user_login).first()

    #new chat
    new_chat = database.Chat(first_member_id = current_user.user_id, second_member_id= user.user_id)
    database.db.session.add(new_chat)
    database.db.session.commit()
    new_message = database.Messages(author_id = user.user_id, chat_id = new_chat.chat_id, text = "Привет. Давай общаться!", read = False, date = cur_time())
    database.db.session.add(new_message)
    database.db.session.commit()
    new_chat.last_message_id = new_message.message_id
    database.db.session.commit()


    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('user.user', user_login=user.login))
    current_user.follow(user)
    database.db.session.commit()
    flash('You are now following %s.' % user_login)
    return redirect(url_for('user.user', user_login=user.login))

@mod.route('/unfollow/<user_login>')
def unfollow(user_login):
    if g.user is None:
        return redirect(url_for('login.login'))
    current_user = database.Users.query.filter_by(user_id=g.user.user_id).first()

    user = database.Users.query.filter_by(login=user_login).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('application.index'))
    if not current_user.is_following(user):
        flash('You are not following this user.')
        return redirect(url_for('user.user', user_login=user.login))
    current_user.unfollow(user)
    database.db.session.commit()
    flash('You stopped to follow %s.' % user_login)
    return redirect(url_for('user.user', user_login=user.login))


@mod.route('/followers/<user_login>')
def followers(user_login):
    if g.user is None:
        return redirect(url_for('login.login'))
    current_user = database.Users.query.filter_by(user_id=g.user.user_id).first()

    user = database.Users.query.filter_by(login=user_login).first()

    if user is None:
        flash('Invalid user.')
        return redirect(url_for('application.index'))

    #list of Follow objects
    followersF = user.followers.all()
    #list of corresponding User objects
    followersU = []
    for follow in followersF:
        followersU.append (database.Users.query.filter_by(user_id=follow.follower_id).first())

    return render_template('followers.html', user=user, current_user=current_user, followers=followersU)

@mod.route('/follows/<user_login>')
def follows(user_login):
    if g.user is None:
        return redirect(url_for('login.login'))
    current_user = database.Users.query.filter_by(user_id=g.user.user_id).first()

    user = database.Users.query.filter_by(login=user_login).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('application.index'))

    #list of Follow objects
    followsF = user.follows.all()
    #list of corresponding Users objects
    followsU = []
    for follow in followsF:
        followsU.append (database.Users.query.filter_by(user_id=follow.followed_id).first())

    return render_template('follows.html', user=user, current_user=current_user, follows=followsU)
    
def cur_time():
    now = datetime.datetime.now()
    return ( (('0'+str(now.hour)) if (now.hour<10) else str(now.hour))+':'+(('0'+str(now.minute)) if (now.minute<10) else str(now.minute))+' '+str(now.day)+'/'+str(now.month))