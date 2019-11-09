import os
import pickle
from math import ceil

from flask import render_template, g, redirect, request, url_for, current_app
from flask_login import current_user
import markdown
from markupsafe import Markup

from app.main.forms import SearchForm

from app.main import bp
from app.models import Jrnl


@bp.before_app_request
def before_request():
    g.search_form = SearchForm()


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home', user=current_user)


@bp.route('/art/<md_file>')
def art_view(md_file):
    with open("app/art/" + md_file + ".md") as f:
        text = f.read()
        content = Markup(markdown.markdown(text, extensions=['fenced_code', 'footnotes', 'toc']))

    return render_template('art_view.html', user=current_user, content=content)


@bp.route('/arts')
def art():
    return render_template('art_list.html', title='Arts', user=current_user)


@bp.route('/dash')
def dash():
    if os.path.isfile(current_app.config['IBM_BACKENDS_PICKLE']):
        f = open(current_app.config['IBM_BACKENDS_PICKLE'], 'rb')
        dr = pickle.load(f)
    else:
        dr = {'tms': None, 'backends': []}

    jrnls = Jrnl.get_news_filter('#qc').limit(10)

    return render_template('dash.html', title='Dash', user=current_user, data=dr, jrnls=jrnls)


@bp.route('/search')
def search():
    per_page = 15
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    jrnls, total = Jrnl.search(g.search_form.q.data, page,
                               per_page)

    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * per_page else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', jrnls=jrnls,
                           next_url=next_url, prev_url=prev_url, page=page, total=ceil(total / per_page))
