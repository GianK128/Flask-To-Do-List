from flask import Blueprint, jsonify, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from todo_list import db
from todo_list.models import User, friend_requests_table

friends = Blueprint('friends', __name__)

@friends.route('search-user/<username>')
def search_user(username):
    query = User.query.filter(User.username.contains(username)).all()
    usernames = [u.username for u in query]
    if current_user.username in usernames: usernames.remove(current_user.username)
    for friend in current_user.friends:
        if friend.username in usernames: usernames.remove(friend.username)
    return jsonify(usernames)

@friends.route('<username>')
def friend_list(username):
    _user = User.query.filter_by(username=username).first()
    requests_received = db.session.query(friend_requests_table).filter_by(second_user_id=current_user.id).all()
    friend_requests = [User.query.get(request.first_user_id) for request in requests_received]
    return render_template('friend_list.html', user=username, friends=_user.friends, requests=friend_requests, friend_count=len(_user.friends))

@login_required
@friends.route('add/<username>')
def add(username):
    _receiver = User.query.filter_by(username=username).first()
    current_user.friend_requests.append(_receiver)
    db.session.commit()
    return redirect(url_for('friends.friend_list', username=current_user.username))

@login_required
@friends.route('request_action/<request_action>')
def request_action(request_action):
    to_user = request.args.get('to_user')
    _sender = User.query.filter_by(username=to_user).first()
    _sender.friend_requests.remove(current_user)
    if request_action == 'accept':
        current_user.friends.append(_sender)
        _sender.friends.append(current_user)
    elif request_action == 'reject':
        flash(f"Rejected {to_user}'s request.", category='info')
    db.session.commit()
    return redirect(url_for('friends.friend_list', username=current_user.username))
