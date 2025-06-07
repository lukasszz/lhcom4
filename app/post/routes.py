import os
from math import ceil

from flask import render_template, flash, redirect, url_for, request, current_app
from flask_login import login_required
import markdown
from markupsafe import Markup
from werkzeug.utils import secure_filename

from app import db
from app.post import bp
from app.post.forms import PostForm
from app.models import Post


def save_header_image(post_id, image_file):
    """Save the header image for a post in its dedicated directory."""
    # Create post directory if it doesn't exist
    post_dir = os.path.join(current_app.root_path, 'static', 'post', str(post_id))
    os.makedirs(post_dir, exist_ok=True)
    
    # Secure the filename and save the file
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(post_dir, filename)
    image_file.save(image_path)
    
    # Return the relative path for storing in the database
    return os.path.join('post', str(post_id), filename)


@bp.route('/post_new', methods=['POST', 'GET'])
@login_required
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, category=form.category.data)
        db.session.add(post)
        db.session.commit()  # Commit to get the post ID
        
        if form.header_image.data:
            image_path = save_header_image(post.id, form.header_image.data)
            post.header_image = image_path
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
        
        if form.header_image.data:
            # Remove old image if it exists
            if post.header_image:
                old_image_path = os.path.join(current_app.root_path, 'static', post.header_image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            image_path = save_header_image(post.id, form.header_image.data)
            post.header_image = image_path
            
        db.session.add(post)
        db.session.commit()
        flash('Successfully edited Post id: ' + str(post.id))
        return redirect(url_for('post.post_list'))
        
    form.title.data = post.title
    form.category.data = post.category
    form.body.data = post.body
    return render_template('post_ed.html', form=form, post=post)


@bp.route('/<int:id>', endpoint='default')
@bp.route('/<int:id>/<string:slug>', endpoint='default_with_slug')
@bp.route('/view/<int:id>')
@bp.route('/view/<int:id>/<string:slug>')
def view(id, slug=None):
    post = Post.query.get_or_404(id)
    # If no slug provided or incorrect slug, redirect to the canonical URL
    if not slug or slug != post.slug:
        return redirect(url_for('post.default_with_slug', id=id, slug=post.slug))
    body = Markup(markdown.markdown(post.body, extensions=['fenced_code', 'footnotes', 'toc']))
    return render_template('post_view.html', title=post.title, body=body, post=post)


@bp.route('/post_list')
def post_list():
    page = request.args.get('page', 1, type=int)
    posts = Post.get_news().paginate(page=page, per_page=9)
    total_pages = ceil(posts.total / posts.per_page)

    return render_template('post_list.html', posts=posts, total_pages=total_pages)
