from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from os.path import abspath, dirname, join

DB_NAME = "usernotes.db"
UPLOAD_FOLDER_PATH = join(abspath(dirname(__file__)), 'static', 'uploads')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c9d1cd6d3e0a4fb54a653b98'
app.config['SECURITY_PASSWORD_SALT'] = '19e2e8d192515eb0c3708d1c'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_PATH

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Se requiere una cuenta.'

from todo_list.routes import routes
from todo_list.auth import auth
from todo_list.list import list
from todo_list.friends import friends

app.register_blueprint(routes, url_prefix='/')
app.register_blueprint(auth, url_prefix='/auth/')
app.register_blueprint(list, url_prefix='/')
app.register_blueprint(friends, url_prefix='/friends/')

from todo_list.models import Item, List, User

@app.context_processor
def utility_processor():
    def get_item_name(item_id):
        return Item.query.get(item_id).content

    def get_list_name(list_id):
        return List.query.get(list_id).name

    def get_username(user_id):
        return User.query.get(user_id).username

    return dict(
        get_item_name = get_item_name,
        get_list_name = get_list_name,
        get_username = get_username
    )
