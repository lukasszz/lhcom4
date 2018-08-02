from app.models import User

u = User(login='lukasz', email='lukasz@lukaszherok.com')
u.set_password('abc')
from app import db

db.session.add(u)
db.session.commit()
