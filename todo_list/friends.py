from flask import Blueprint, jsonify, render_template
from todo_list import db
from todo_list.models import User

friends = Blueprint('friends', __name__)

@friends.route('search-user/<username>')
def search_user(username):
    query = User.query.filter(User.username.contains(username)).all()
    usernames = [u.username for u in query]
    return jsonify(usernames)

@friends.route('<username>')
def friend_list(username):
    _user = User.query.filter_by(username=username).first()
    return render_template('friend_list.html', user=username, friends=_user.relations, friend_count=len(_user.relations))
