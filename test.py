import unittest

from app import db, create_app
from app.models import User, Jrnl


from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None

class JrnlModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_post(self):
        a = User(username='lukasz')
        db.session.add(a)
        db.session.commit()

        p = Jrnl(author=a, body='Abc')
        db.session.add(p)
        db.session.commit()

        self.assertEqual(1, Jrnl.get_news().count())

        p = Jrnl(author=a, body='Bcd')
        db.session.add(p)
        db.session.commit()

        self.assertEqual(2, Jrnl.get_news().count())
        self.assertEqual('Bcd', Jrnl.get_news().first().body)