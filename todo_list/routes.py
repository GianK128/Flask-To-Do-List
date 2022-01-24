from flask import render_template, Blueprint
from flask_login import current_user
from sqlalchemy import desc
from todo_list.models import User, ActivityLog, friends_table

routes = Blueprint('routes', __name__)

@routes.route('/')
@routes.route('/home')
def home():
    activities = []
    if current_user.is_authenticated:
        # Query (parecida):
        # SELECT * FROM activity_log INNER JOIN user, friend_relationship where (first_user_id == 1 and second_user_id == user_id and second_user_id == user.id) or (first_user_id == 1 and activity_log.user_id == 1 and user.id == activity_log.user_id) ORDER BY activity_log.date DESC
        activities = ActivityLog.query\
            .join(User)\
            .filter(
                ((ActivityLog.user_id == friends_table.c.second_user_id) & (friends_table.c.first_user_id == current_user.id)) |
                (ActivityLog.user_id == current_user.id)
            )\
            .order_by(desc(ActivityLog.date))\
            .all()
    return render_template('home.html', activities = activities)
