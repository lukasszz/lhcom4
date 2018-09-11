## TODO

[x] Integrating Search for jrnl
[ ] ResearchGate 
[ ] Think what I need: activites, jrnl, blog, reads, tweets.... phisycs, software dev, business

[ ] Jrnl #hashtag +project 
[ ] Deploy for production

[ ] Git-hub
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