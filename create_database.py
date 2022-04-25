from todo_list import db
from todo_list.models import User

db.create_all()

admin = User(username="admin", email="giankeberlein.dev@gmail.com", password="password")

db.session.add_all([admin])
db.session.commit()
