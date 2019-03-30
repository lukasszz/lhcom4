## TODO

[x] 	87.98.239.5
[x] Deploy for production 
    [x] Setup server
    [x] Disalbe debug mode
    [x] Domain
    
[x] https
[x] Markdown support
[ ] Think what I need: activites, jrnl, blog, reads, tweets.... phisycs, software dev, business

[ ] Jrnl tags: #hashtag +project 
[ ] favicon

[ ] Cookies (?)
[ ] Navbar - select active link
[ ] Move configuration to .env and add Config to the repo (instead of creating config sample)
[ ] Jrnl different colors for each card (random or by category)
[ ] Jrnl list move navbar to the center
[ ] Search nav i disappearing in smaller view
[ ] Jrnl Random border colors: (https://getbootstrap.com/docs/4.0/utilities/borders/#border-color) 
[ ] Flashes special box #base.html
[ ] error pages https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
[ ] sending errors by e-mail
[ ] should I download all the css files localy?

## DONE
[x] Add to github
[x] Integrating Search for jrnl
[x] ResearchGate 
[x] Enable elasticsearch
[x] blueprint for jrnl
[x] blueprint for auth
[x] Jrnl list pagination
[x] Jrnl nav bar facelift
[x] Jrnl list page
[x] Index page content
[x] Nav bar for menu #base.html
[x] Login template
[x] post_ed template adjust for css
[x] Base page withotut body #index.html

## DOC
- Jrnl - short tweets about what I've done (Tweeter)
- Notes - my knowledge base (auto post to Jrnl)
- Arts - Publications and longer posts
- Shares - links to things I read/saw on the Internet (FB Like) 
- About - CV (Linked In)
- Workspace - links to projcetcs on BitBucket, GitHub, (resources for PhD)
- Books


## JRNL
### 2019-01-19 1910
$ sudo certbot --nginx certonly
IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   Your key file has been saved at:
   Your cert will expire on 2019-04-10. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot
   again. To non-interactively renew *all* of your certificates, run
   "certbot renew"

$ [root@serwer-1 lhcom4]# ./update_and_reload.sh

### 2018-10-15
Installed ssl certificate from letsencrypt.org with just:


$ sudo dnf install certbot-nginx
$ sudo certbot --nginx

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

You should test your configuration at:
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   Your key file has been saved at:
   Your cert will expire on 2019-01-13. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew *all* of
   your certificates, run "certbot renew"

### 2018-10-02
Disable SELinux.
certs where moved from /home/lukasz/certs to /etc/nginx (selinux problem)

(venv) [lukasz@serwer-1 lhcom4]$ sudo mkdir /run/uwsgi
(venv) [lukasz@serwer-1 lhcom4]$ sudo chown lukasz:lukasz /run/uwsgi


### 2018-09-13
Project add to github for easier deployment.
Just created empty repo on github and pushed my local repo with:
```
git remote add origin https://github.com/(...).git
git push -u origin master

```

### 2018-10-04
Deployed on linux.
$ systemctl start lhcom4.uwsgi.service
$ systemctl start nginx

Configuration:
/etc/nginx/
    nginx.conf
    conf.d
/etc/systemd
lhcom4/uwsgi.ini

Logs:
/var/log/uwsgi
journalctl -ex

### 2018-09-11
Runing the app in console:
``` 
import app
a = app.create_app()
a.app_context().push()

import app.models as m
```

### 2018-08-19
Instalation of elasticsearch. The offcial dnf package for Fedora is broken. Installed it through:
https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html

### 2018-08-08
Facelift. It was enough to download hacker theme [2] into `app/static` dir. Then merge its `index.html`
with `base.html`. Adding styles to my templates requires manually point out the css class, eg.:
```
{{ form.post(cols=32, rows=4, class="form-control") }}<br>
``` 

## REFS
[1] https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
[2] https://hackerthemes.com/bootstrap-themes/neon-glow
[3] https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html
