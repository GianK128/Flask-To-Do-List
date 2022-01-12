from todo_list import db
from todo_list.models import User

db.create_all()

admin = User(username="admin", email="admin@example.com", password="password")
user = User(username="user", email="user@example.com", password="password")

db.session.add_all([admin, user])
db.session.commit()

# _user = User.query.get(1)
# print(_user.relations)
# print(_user.subrelations)

# _user = User.query.get(2)
# print(_user.relations)
# print(_user.subrelations)
