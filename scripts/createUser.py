from app.models import User


u = User(username='lukasz', email='lukasz@lukaszherok.com')
u.set_password('')

from app import create_app, db
app = create_app()
app.app_context().push()

db.session.add(u)
db.session.commit()
