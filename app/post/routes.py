from math import ceil

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required
import markdown
from markupsafe import Markup

from app import db
from app.post import bp
from app.post.forms import PostForm
from app.models import Post


@bp.route('/post_new', methods=['POST', 'GET'])
@login_required
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, category=form.category.data)
        db.session.add(post)
        db.session.commit()
        flash('Added new Post entry!')
        return redirect(url_for('post.post_list'))
    return render_template('post_ed.html', form=form)


@bp.route('/post_ed/<int:id>', methods=['POST', 'GET'])
@login_required
def post_ed(id):
    form = PostForm()
    post = Post.query.get(id)

    if form.validate_on_submit():
        post.body = form.body.data
        post.category = form.category.data
        post.title = form.title.data
        db.session.add(post)
        db.session.commit()
        flash('Sucessfuly edited Post id: ' + str(post.id))
        return redirect(url_for('post.post_list'))
    form.title.data = post.title
    form.category.data = post.category
    form.body.data = post.body
    return render_template('post_ed.html', form=form)


@bp.route('/view/<int:id>/<title>')
def view(id, title):
    post = Post.query.get(id)
    body = Markup(markdown.markdown(post.body, extensions=['fenced_code', 'footnotes', 'toc']))

    return render_template('post_view.html', title=post.title, body=body, post=post)


@bp.route('/post_list')
def post_list():
    page = request.args.get('page', 1, type=int)
    posts = Post.get_news().paginate(page, 9, False)
    total_pages = ceil(posts.total / posts.per_page)

    return render_template('post_list.html', posts=posts, total_pages=total_pages)
