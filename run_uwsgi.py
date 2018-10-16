#!/usr/bin/env bash
export FLASK_APP=microblog.py

# uwsgi --socket 127.0.0.1:3031 --wsgi-file microblog.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191
# uwsgi --http 127.0.0.1:3031 --wsgi-file microblog.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191

# uwsgi -s /run/uwsgi/lhcom4.socket --wsgi-file microblog.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191

uwsgi --ini uwsgi.ini

