from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from app.search import query_index
from hashlib import md5
import re


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = {}
        for i in range(len(ids)):
            when.update({ids[i]: i})
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    jrnl = db.relationship('Jrnl', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))


class Jrnl(SearchableMixin, db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

    @staticmethod
    def get_news():
        return Jrnl.query.order_by(Jrnl.id.desc())

    @staticmethod
    def get_news_filter(like):
        return Jrnl.query.filter(Jrnl.body.contains(like)).order_by(Jrnl.id.desc())


def slugify(text):
    # Convert to lowercase and replace spaces with hyphens
    text = text.lower()
    # Replace Polish characters
    text = text.replace('ą', 'a').replace('ę', 'e').replace('ś', 's')
    text = text.replace('ć', 'c').replace('ó', 'o').replace('ł', 'l')
    text = text.replace('ż', 'z').replace('ź', 'z').replace('ń', 'n')
    # Remove special characters and replace spaces with hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


class Post(SearchableMixin, db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    abstract = db.Column(db.String(500))  # Abstract/description field
    body = db.Column(db.String())
    category = db.Column(db.String(20))
    header_image = db.Column(db.String(200))  # URL or path to the header image
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Post {}>'.format(self.title)

    @property
    def slug(self):
        return slugify(self.title)

    @property
    def excerpt(self):
        """Return abstract if available, otherwise generate a short excerpt from the post body."""
        if self.abstract and self.abstract.strip():
            return self.abstract
        
        # Fallback to generating excerpt from body
        import re
        # Remove markdown syntax and get plain text
        text = re.sub(r'[#*`_\[\]()]', '', self.body)
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Truncate to about 150 characters
        if len(text) > 150:
            text = text[:150].rsplit(' ', 1)[0] + '...'
        return text

    @staticmethod
    def get_news():
        return Post.query.order_by(Post.id.desc())

    @staticmethod
    def get_new_jrnls():
        return Jrnl.query.filter(Jrnl.body.contains('#soft')).order_by(Jrnl.id.desc())

    @staticmethod
    def get_new_posts():
        return Post.query.filter(Post.category == 'softdevel').order_by(Post.id.desc())
