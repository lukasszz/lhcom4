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
elif 'els_search' == command:
    q = sys.argv[2]
    page = 1
    per_page = 15
    jrnls, total = Jrnl.search(q, page, per_page)
    print("Total: " + str(total['value']))
    print(jrnls)
else:
    print("Command '" + command + "' not found")

print('Koniec')

