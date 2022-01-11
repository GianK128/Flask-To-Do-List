from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

DB_NAME = "usernotes.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'c9d1cd6d3e0a4fb54a653b98'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

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
app.register_blueprint(list, url_prefix='/lists/')
app.register_blueprint(friends, url_prefix='/friends/')

