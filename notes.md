## TODO
[x] Nav bar for menu #base.html
[x] Login template
[ ] post_ed template adjust for css
[ ] Index page withotut body #index.html
[ ] Flashes special box #base.html
[ ] Post list page
[ ] Next chapter

[ ] Think what I need: activites, jrnl, blog, reads, tweets.... phisycs, software dev, business

[ ] Deploy for production

[ ] error pages https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
[ ] sending errors by e-mail
[ ] should I download all the css files localy?

## JRNL

### 2018-08-08
Facelift. It was enough to download hacker theme [2] into `app/static` dir. Then merge its `index.html`
with `base.html`. Adding styles to my templates requires manually point out the css class, eg.:
```
{{ form.post(cols=32, rows=4, class="form-control") }}<br>
``` 

## REFS
[1] https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
[2] https://hackerthemes.com/bootstrap-themes/neon-glow/#!