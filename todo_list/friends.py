from flask import Blueprint, jsonify, render_template, redirect, url_for, escape
from flask_login import login_required, current_user
from todo_list import db
from todo_list.models import User, UserRelationship

friends = Blueprint('friends', __name__)

@friends.route('search-user/<username>')
def search_user(username):
    query = User.query.filter(User.username.contains(username)).all()
    usernames = [u.username for u in query]
    return jsonify(usernames)

@friends.route('<username>')
def friend_list(username):
    _user = User.query.filter_by(username=username).first()
    friends = []
    for relation in _user.relations:
        friends.append(User.query.get(relation.second_user_id))
    for subrelation in _user.subrelations:
        friends.append(User.query.get(subrelation.first_user_id))
    return render_template('friend_list.html', user=username, friends=friends, friend_count=len(_user.relations))

@login_required
@friends.route('add/<username>')
def add(username):
    _receiver = User.query.filter_by(username=username).first()
    association = UserRelationship(second_user_id=_receiver.id, relation_status=1)
    current_user.relations.append(association)
    db.session.commit()
    return redirect(url_for('friends.friend_list', username=current_user.username))
