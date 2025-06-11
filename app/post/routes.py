import os
from math import ceil

from flask import render_template, flash, redirect, url_for, request, current_app, jsonify
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


def save_content_images(post_id, content_images_field):
    """Save content images and return markdown syntax for each."""
    if not content_images_field:
        return []
    
    # Create post directory if it doesn't exist
    post_dir = os.path.join(current_app.root_path, 'static', 'post', str(post_id))
    os.makedirs(post_dir, exist_ok=True)
    
    markdown_snippets = []
    
    # Handle multiple files from a single FileField
    image_files = request.files.getlist('content_images')
    
    for image_file in image_files:
        if image_file.filename:  # Check if file was actually uploaded
            # Secure the filename and save the file
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(post_dir, filename)
            image_file.save(image_path)
            
            # Generate markdown syntax
            relative_path = url_for('static', filename=f'post/{post_id}/{filename}')
            markdown_syntax = f'![Image description]({relative_path})'
            markdown_snippets.append(markdown_syntax)
    
    return markdown_snippets


def get_post_images(post_id):
    """Get all images from a post's directory."""
    post_dir = os.path.join(current_app.root_path, 'static', 'post', str(post_id))
    
    if not os.path.exists(post_dir):
        return []
    
    images = []
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
    
    for filename in os.listdir(post_dir):
        if any(filename.lower().endswith(ext) for ext in allowed_extensions):
            relative_path = url_for('static', filename=f'post/{post_id}/{filename}')
            images.append({
                'filename': filename,
                'url': relative_path,
                'markdown': f'![Image description]({relative_path})',
                'html': f'<figure>\n  <img src="{relative_path}" alt="Opis obrazu" />\n  <figcaption>Rys 0. Krótki podpis pod ilustracją</figcaption>\n</figure>'
            })
    
    return images


@bp.route('/post_new', methods=['POST', 'GET'])
@login_required
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, abstract=form.abstract.data, body=form.body.data, category=form.category.data)
        
        # Set timestamp if provided, otherwise use default
        if form.timestamp.data:
            post.timestamp = form.timestamp.data
            
        db.session.add(post)
        db.session.commit()  # Commit to get the post ID
        
        # Handle header image
        if form.header_image.data:
            image_path = save_header_image(post.id, form.header_image.data)
            post.header_image = image_path
            db.session.commit()
        
        # Handle content images
        if 'content_images' in request.files and request.files.getlist('content_images')[0].filename:
            markdown_snippets = save_content_images(post.id, None)
            if markdown_snippets:
                flash(f'Images uploaded! Copy this markdown: {" ".join(markdown_snippets)}')
            
        flash('Added new Post entry!')
        return redirect(url_for('post.post_list'))
    return render_template('post_ed.html', form=form, post_images=[])


@bp.route('/post_ed/<int:id>', methods=['POST', 'GET'])
@login_required
def post_ed(id):
    form = PostForm()
    post = Post.query.get(id)

    if form.validate_on_submit():
        post.body = form.body.data
        post.category = form.category.data
        post.title = form.title.data
        post.abstract = form.abstract.data
        
        # Update timestamp if provided
        if form.timestamp.data:
            post.timestamp = form.timestamp.data
        
        # Handle header image
        if form.header_image.data:
            # Remove old image if it exists
            if post.header_image:
                old_image_path = os.path.join(current_app.root_path, 'static', post.header_image)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
            
            image_path = save_header_image(post.id, form.header_image.data)
            post.header_image = image_path
        
        # Handle content images
        if 'content_images' in request.files and request.files.getlist('content_images')[0].filename:
            markdown_snippets = save_content_images(post.id, None)
            if markdown_snippets:
                flash(f'Images uploaded! Copy this markdown: {" ".join(markdown_snippets)}')
            
        db.session.add(post)
        db.session.commit()
        flash('Successfully edited Post id: ' + str(post.id))
        return redirect(url_for('post.default_with_slug', id=post.id, slug=post.slug))
        
    form.title.data = post.title
    form.abstract.data = post.abstract
    form.category.data = post.category
    form.body.data = post.body
    form.timestamp.data = post.timestamp
    
    # Get list of images for this post
    post_images = get_post_images(post.id)
    
    return render_template('post_ed.html', form=form, post=post, post_images=post_images)


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


@bp.route('/upload_image/<int:post_id>', methods=['POST'])
@login_required
def upload_image(post_id):
    """AJAX endpoint for uploading images during editing."""
    post = Post.query.get_or_404(post_id)
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Validate file extension
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    if not any(image_file.filename.lower().endswith(ext) for ext in allowed_extensions):
        return jsonify({'error': 'Invalid file format. Only JPG, PNG, and WebP are allowed.'}), 400
    
    # Save the image
    post_dir = os.path.join(current_app.root_path, 'static', 'post', str(post_id))
    os.makedirs(post_dir, exist_ok=True)
    
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(post_dir, filename)
    image_file.save(image_path)
    
    # Generate markdown syntax
    relative_path = url_for('static', filename=f'post/{post_id}/{filename}')
    markdown_syntax = f'![Image description]({relative_path})'
    
    return jsonify({
        'success': True,
        'markdown': markdown_syntax,
        'url': relative_path
    })


@bp.route('/upload_content_images/<int:post_id>', methods=['POST'])
@login_required
def upload_content_images(post_id):
    """AJAX endpoint for uploading multiple content images automatically."""
    post = Post.query.get_or_404(post_id)
    
    if 'content_images' not in request.files:
        return jsonify({'error': 'No images provided'}), 400
    
    uploaded_images = []
    image_files = request.files.getlist('content_images')
    
    # Validate and process each file
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
    
    for image_file in image_files:
        if image_file.filename == '':
            continue
            
        # Validate file extension
        if not any(image_file.filename.lower().endswith(ext) for ext in allowed_extensions):
            return jsonify({'error': f'Invalid file format for {image_file.filename}. Only JPG, PNG, and WebP are allowed.'}), 400
        
        # Save the image
        post_dir = os.path.join(current_app.root_path, 'static', 'post', str(post_id))
        os.makedirs(post_dir, exist_ok=True)
        
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(post_dir, filename)
        image_file.save(image_path)
        
        # Generate URLs and syntax
        relative_path = url_for('static', filename=f'post/{post_id}/{filename}')
        markdown_syntax = f'![Image description]({relative_path})'
        html_syntax = f'<figure>\n  <img src="{relative_path}" alt="Opis obrazu" />\n  <figcaption>Rys 0.Krótki podpis pod ilustracją</figcaption>\n</figure>'
        
        uploaded_images.append({
            'filename': filename,
            'url': relative_path,
            'markdown': markdown_syntax,
            'html': html_syntax
        })
    
    return jsonify({
        'success': True,
        'images': uploaded_images,
        'count': len(uploaded_images)
    })


@bp.route('/delete_image/<int:post_id>/<filename>', methods=['DELETE'])
@login_required
def delete_image(post_id, filename):
    """AJAX endpoint for deleting uploaded images."""
    post = Post.query.get_or_404(post_id)
    
    # Secure the filename
    filename = secure_filename(filename)
    
    # Build file path
    post_dir = os.path.join(current_app.root_path, 'static', 'post', str(post_id))
    file_path = os.path.join(post_dir, filename)
    
    # Check if file exists and delete it
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return jsonify({
                'success': True,
                'message': f'Image {filename} deleted successfully'
            })
        except OSError as e:
            return jsonify({'error': f'Failed to delete file: {str(e)}'}), 500
    else:
        return jsonify({'error': 'File not found'}), 404
