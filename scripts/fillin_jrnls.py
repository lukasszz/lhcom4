from app import app, db
from app.models import User, Jrnl

user = User.query.first()
print(user)

for i in range(10):
    j = Jrnl(body="Jrnl " + str(i) + " ga kjkljlk fakl lkfdajk lfjkfdaj fdaj fkajf dakljf akjf akfj kafj salkfj alkfjsa lkf jsa")
    db.session.add(j)

db.session.commit()
