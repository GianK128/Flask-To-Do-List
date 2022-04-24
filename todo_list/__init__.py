from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from os import environ
from os.path import abspath, dirname, join
import datetime

DB_NAME = "usernotes.db"
UPLOAD_FOLDER_PATH = join(abspath(dirname(__file__)), 'static', 'uploads')

app = Flask(__name__)
app.config['SECRET_KEY'] = environ['APP_SECRET_KEY']
app.config['SECURITY_PASSWORD_SALT'] = environ['APP_SECURITY_PASSWORD_SALT']
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_PATH

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = environ['APP_MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = environ['APP_MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = environ['APP_MAIL_USERNAME']

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
mail = Mail(app)

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Se requiere una cuenta.'

from todo_list.routes import routes
from todo_list.auth import auth
from todo_list.list import list
from todo_list.friends import friends
from todo_list.settings import settings

app.register_blueprint(routes, url_prefix='/')
app.register_blueprint(auth, url_prefix='/auth/')
app.register_blueprint(list, url_prefix='/')
app.register_blueprint(friends, url_prefix='/friends/')
app.register_blueprint(settings, url_prefix='/settings/')

from todo_list.models import Item, List, User, friend_requests_table

@app.context_processor
def utility_processor():
    def get_item_name(item_id):
        return Item.query.get(item_id).content

    def get_list_name(list_id):
        return List.query.get(list_id).name

    def get_username(user_id):
        return User.query.get(user_id).username

    def get_pic_path_by_id(user_id):
        return User.query.get(user_id).pic_path

    def get_date_from_ordinal(ordinal_date):
        return datetime.date.fromordinal(ordinal_date)

    def get_completed_items_string(list):
        total_items = len(list.items)
        completed_items = 0

        for item in list.items:
            if item.completed:
                completed_items += 1
        
        return f"{completed_items:02d}/{total_items:02d}"

    def get_length_of(element):
        return len(element)

    def censor_email(email):
        s = email.split('@')
        s[0] = s[0][0] + "*" * len(s[0][0::])
        s1 = s[1].split('.')
        s1[0] = s1[0][0] + "*" * len(s1[0][0::])
        s[1] = ".".join(s1)
        return "@".join(s)

    def get_requests_number(of_user):
        requests = db.session.query(friend_requests_table).filter_by(second_user_id=of_user.id).all()
        return len(requests)

    def is_friend(user, list_holder):
        return user in list_holder.friends

    def is_requested(user, list_holder):
        return user in list_holder.friend_requests

    return dict(
        get_item_name = get_item_name,
        get_list_name = get_list_name,
        get_username = get_username,
        get_date_from_ordinal = get_date_from_ordinal,
        get_pic_path_by_id = get_pic_path_by_id,
        get_completed_items_string = get_completed_items_string,
        get_length_of = get_length_of,
        censor_email = censor_email,
        get_requests_number = get_requests_number,
        is_friend = is_friend,
        is_requested = is_requested
    )
