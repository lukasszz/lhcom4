#!/usr/bin/env bash
export FLASK_APP=microblog.py
export FLASK_DEBUG=1
#sudo systemctl start elasticsearch
echo "Notice: Without Elastic search"
flask run --port 5001

