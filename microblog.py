from app import create_app
from app.models import User, Jrnl
from config import Config

app = create_app(Config)


@app.shell_context_processor
def make_shell_context():
    return {'db': app.db, 'User': User, 'Jrnl': Jrnl}
