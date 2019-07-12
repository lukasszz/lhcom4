import sys

from app import create_app, db
from app.models import Jrnl

if len(sys.argv) < 2:
    print('No command specified')
    exit(1)

command = sys.argv[1]

app = create_app()
app_context = app.app_context()
app_context.push()

if 'els_reindex' == command:
    Jrnl.reindex()
    print('Elasticsearch reindexed')

