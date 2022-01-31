from flask import Blueprint, jsonify, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from todo_list import db
from todo_list.decorators import confirm_required
from todo_list.models import User, friend_requests_table, ActivityLog

friends = Blueprint('friends', __name__)

@friends.route('search-user')
@login_required
def search_user():
    username = request.args.get('user')
    query = User.query.filter(User.username.contains(username)).all()

    if current_user in query: query.remove(current_user)
    for friend in current_user.friends:
        if friend in query: 
            query.remove(friend)

    usernames = [[u.username, u in current_user.friend_requests] for u in query]
    return jsonify(usernames)

@friends.route('<username>')
@login_required
@confirm_required
def friend_list(username):
    _user = User.query.filter_by(username=username).first()
    requests_received = db.session.query(friend_requests_table).filter_by(second_user_id=current_user.id).all()
    friend_requests = [User.query.get(request.first_user_id) for request in requests_received]
    return render_template('friend_list.html', user=username, friends=_user.friends, requests=friend_requests, friend_count=len(_user.friends))

@friends.route('add')
@login_required
@confirm_required
def add():
    username = request.args.get('user')
    _receiver = User.query.filter_by(username=username).first()
    current_user.friend_requests.append(_receiver)
    db.session.commit()
    return jsonify(success=True)

@friends.route('request')
@login_required
@confirm_required
def request_action():
    request_action = request.args.get('action')
    to_user = request.args.get('to_user')
    _sender = User.query.filter_by(username=to_user).first()
    _sender.friend_requests.remove(current_user)
    if request_action == 'accept':
        current_user.friends.append(_sender)
        _sender.friends.append(current_user)
        _log = ActivityLog(
            type = 3,
            friend_id = _sender.id
        )
        db.session.add(_log)
        current_user.activities.append(_log)
    elif request_action == 'reject':
        flash(f"Rejected {to_user}'s request.", category='info')
    db.session.commit()
    return jsonify(success=True)
