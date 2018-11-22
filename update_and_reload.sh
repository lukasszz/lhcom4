#!/bin/bash

git pull
/home/lukasz/lhcom4/venv/bin/flask db upgrade

echo 'Stoping nginx...'
sudo systemctl stop nginx
echo 'Restarting lhcom4.uwsgi (if failed kill and start manuall)...'
sudo systemctl restart lhcom4.uwsgi.service
sudo systemctl status lhcom4.uwsgi.service

echo 'Starting nginx...'
sudo systemctl start nginx

echo 'Finished. Enjoy'

