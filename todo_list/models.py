from sqlalchemy.orm import backref, relationship
from sqlalchemy.orm.relationships import foreign
from todo_list import db, bcrypt, login_manager
from flask_login import UserMixin
from sqlalchemy.sql import func

friends_table = db.Table("friend_relationship", db.Model.metadata,
    db.Column('first_user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
    db.Column('second_user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True)
)
friend_requests_table = db.Table("friend_request", db.Model.metadata,
    db.Column('first_user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True),
    db.Column('second_user_id', db.Integer(), db.ForeignKey('user.id'), primary_key=True)
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    lists = db.relationship('List', backref='user', lazy=True, cascade="all, delete")
    friends = db.relationship('User',
        secondary = friends_table,
        primaryjoin = id == friends_table.c.first_user_id,
        secondaryjoin = id == friends_table.c.second_user_id,
        cascade = "all, delete",
        backref = backref('users')
    )
    friend_requests = db.relationship('User',
        secondary = friend_requests_table,
        primaryjoin = id == friend_requests_table.c.first_user_id,
        secondaryjoin = id == friend_requests_table.c.second_user_id,
        cascade = "all, delete",
        backref = backref('users_requested')
    )
    activities = db.relationship('ActivityLog',
        cascade = "all, delete",
        backref = backref('user')
    )

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
    items = db.relationship('Item', backref='list', lazy=True, cascade="all, delete")
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

class ActivityLog(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    type = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer())
    list_id = db.Column(db.Integer(), db.ForeignKey('list.id'))
    item_id = db.Column(db.Integer(), db.ForeignKey('item.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"<Post ({self.id}) - Type {self.type}, created at {self.date}>"