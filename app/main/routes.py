import os
import pickle
from math import ceil

from flask import render_template, g, redirect, request, url_for, current_app
from flask_login import current_user
import markdown
from markupsafe import Markup

from app.main.forms import SearchForm

from app.main import bp
from app.models import Jrnl, Post


@bp.before_app_request
def before_request():
    g.search_form = SearchForm()


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home', user=current_user)


@bp.route('/art/<md_file>')
def art_view(md_file):
    with open(current_app.root_path + "/art/" + md_file + ".md") as f:
        text = f.read()
        content = Markup(markdown.markdown(text, extensions=['fenced_code', 'footnotes', 'toc']))

    return render_template('art_view.html', user=current_user, content=content)


@bp.route('/arts')
def art():
    return render_template('art_list.html', title='Arts', user=current_user)


@bp.route('/dash')
def dash():
    ibm_pickle_path = current_app.config.get('IBM_BACKENDS_PICKLE')
    if ibm_pickle_path and os.path.isfile(ibm_pickle_path):
        f = open(ibm_pickle_path, 'rb')
        dr = pickle.load(f)
    else:
        dr = {'tms': None, 'backends': []}

    jrnls = Jrnl.get_news_filter('#qc').limit(10)
    
    # Get latest posts for the dashboard panel (only quantum category)
    latest_posts = Post.query.filter_by(category='quantum').order_by(Post.timestamp.desc()).limit(3).all()

    return render_template('dash.html', title='Dash', user=current_user, data=dr, jrnls=jrnls, latest_posts=latest_posts)


@bp.route('/softdevel')
def softdevel():

    jrnls = Post.get_new_jrnls().limit(3)
    posts = Post.get_new_posts().limit(3)

    return render_template('softdevel.html', title='Sofware development', user=current_user, posts=posts, jrnls=jrnls)


@bp.route('/search')
def search():
    # csrf filed error
    #if not g.search_form.validate():
    #    return redirect(url_for('main.explore'))

    query = g.search_form.q.data
    per_page = 20
    page = request.args.get('page', 1, type=int)

    jrnls, total = Jrnl.search(query, page, per_page)

    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * per_page else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None

    return render_template('search.html', title='Search', jrnls=jrnls,
                           next_url=next_url, prev_url=prev_url, page=page, total=ceil(total / per_page))
