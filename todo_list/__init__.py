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
app.config['SECRET_KEY'] = 'c9d1cd6d3e0a4fb54a653b98'
app.config['SECURITY_PASSWORD_SALT'] = '19e2e8d192515eb0c3708d1c'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_PATH

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = environ['APP_MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = environ['APP_MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = 'giankeberlein.dev@gmail.com'

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

from todo_list.models import Item, List, User

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

    return dict(
        get_item_name = get_item_name,
        get_list_name = get_list_name,
        get_username = get_username,
        get_date_from_ordinal = get_date_from_ordinal,
        get_pic_path_by_id = get_pic_path_by_id,
        get_completed_items_string = get_completed_items_string,
        get_length_of = get_length_of
    )
