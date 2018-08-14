## TODO

[x] Jrnl list pagination

[ ] Jrnl nav bar facelift
[ ] Next chapter

[ ] Think what I need: activites, jrnl, blog, reads, tweets.... phisycs, software dev, business

[ ] Jrnl hashtags
[ ] Deploy for production

[ ] Git-hub
[ ] Jrnl different colors for each card (random or by category)
[ ] Jrnl list move navbar to the center
[ ] Search nav i disappearing in smaller view
[ ] Jrnl Random border colors: (https://getbootstrap.com/docs/4.0/utilities/borders/#border-color) 
[ ] Flashes special box #base.html
[ ] error pages https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-error-handling
[ ] sending errors by e-mail
[ ] should I download all the css files localy?

## DONE
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


## JRNL

### 2018-08-08
Facelift. It was enough to download hacker theme [2] into `app/static` dir. Then merge its `index.html`
with `base.html`. Adding styles to my templates requires manually point out the css class, eg.:
```
{{ form.post(cols=32, rows=4, class="form-control") }}<br>
``` 

## REFS
[1] https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-v-user-logins
[2] _https://hackerthemes.com/bootstrap-themes/neon-glow/#!_