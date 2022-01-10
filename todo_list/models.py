from sqlalchemy.orm import relationship
from todo_list import db, bcrypt, login_manager
from flask_login import UserMixin
from sqlalchemy.sql import func

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    lists = db.relationship('List', backref='user', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text):
        self.password_hash = bcrypt.generate_password_hash(plain_text).decode('utf-8')
    
    def check_password_correct(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    def __repr__(self):
        return f"<User ({self.id}) - {self.username}>"

class List(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean(), default=False)
    items = db.relationship('Item', backref='list', lazy=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<List ({self.id}) - Owned by {self.user_id}>"

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    date_written = db.Column(db.DateTime(timezone=True), default=func.now())
    completed = db.Column(db.Boolean(), default=False)
    list_id = db.Column(db.Integer(), db.ForeignKey('list.id'))

    def __repr__(self):
        return f"<Item ({self.id}) - Contained in list {self.list_id}>"
