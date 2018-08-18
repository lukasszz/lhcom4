from flask import Blueprint

bp = Blueprint('jrnl', __name__, template_folder='templates')

from app.jrnl import routes
