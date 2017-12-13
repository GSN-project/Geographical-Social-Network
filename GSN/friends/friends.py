from flask import Blueprint, request, redirect, url_for, render_template,g
from GSN import database

mod = Blueprint('friends', __name__, template_folder='templates')

@mod.route("/friends", methods = ['POST', 'GET'])
def friends():
    if g.user is None:
        return redirect(url_for('login.login'))

    user = database.Users.query.filter_by(user_id=g.user.user_id).first()
    
    followersF = user.followers.all()
    followsF = user.follows.all()
    #Follow objects to Users objects
    followsU = []
    for follow in followsF:
        followsU.append (database.Users.query.filter_by(user_id=follow.followed_id).first())
    
    followersU = []
    for follow in followersF:
        followersU.append (database.Users.query.filter_by(user_id=follow.follower_id).first())

    res_friends = []
    res_followers = []
    for x in followersU:
        if x in followsU:
            res_friends.append(x);
            followsU.remove(x);
        else:
            res_followers.append(x);

    #print ('Followers:', res_followers)
    #print ('Friends:', res_friends)
    #print ('Follows:', follows)
    return render_template('Friends.html', friends=res_friends, followers=res_followers, follows=followsU, current_user=user, username=g.user.login)