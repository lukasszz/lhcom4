import unittest

from app import app, db
from app.models import User, Post


class PostModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_post(self):
        a = User(username='lukasz')
        db.session.add(a)
        db.session.commit()

        p = Post(author=a, body='Abc')
        db.session.add(p)
        db.session.commit()

        self.assertEqual(1, Post.get_news().count())

        p = Post(author=a, body='Bcd')
        db.session.add(p)
        db.session.commit()

        self.assertEqual(2, Post.get_news().count())
        self.assertEqual('Bcd', Post.get_news().first().body)