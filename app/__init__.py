from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from elasticsearch import Elasticsearch
import certifi

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
# mail = Mail()
# bootstrap = Bootstrap()
moment = Moment()
# babel = Babel()


# app = Flask(__name__)
# app.config.from_object(Config)

# db = SQLAlchemy(app)

# migrate = Migrate(app, db)

# login = LoginManager(app)
# login.login_view = 'login'

# moment = Moment(app)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    moment.init_app(app)

    app.elasticsearch = None
    if app.config['ELASTICSEARCH_URL'] is not None:
        if 'http://' == app.config['ELASTICSEARCH_URL'][:7]:
            app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']])
        elif 'https://' == app.config['ELASTICSEARCH_URL'][:8]:
            app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']], use_ssl=True, ca_certs=certifi.where())

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.jrnl import bp as jrnl_bp
    app.register_blueprint(jrnl_bp, url_prefix='/jrnl')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from flask_pagedown import PageDown
    app.pagedown = PageDown()
    app.pagedown.init_app(app)

    from flaskext.markdown import Markdown
    Markdown(app,  extensions=['fenced_code', 'footnotes', 'toc'])

    return app

from app import models