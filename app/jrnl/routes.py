from math import ceil

from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required

from app import app, db
from app.jrnl.forms import JrnlForm
from app.models import Jrnl
from app.jrnl import bp


@bp.route('/jrnl_ed', methods=['POST', 'GET'])
@login_required
def jrnl_ed():
    form = JrnlForm()
    if form.validate_on_submit():
        jrnl = Jrnl(body=form.jrnl.data, author=current_user)
        db.session.add(jrnl)
        db.session.commit()
        flash('Added new Jrnl entry!')
        return redirect(url_for('main.index'))
    return render_template('jrnl_ed.html', form=form)


@bp.route('/jrnl_list')
def jrnl_list():
    page = request.args.get('page', 1, type=int)
    jrnls = Jrnl.get_news().paginate(page, 9, False)
    total_pages = ceil(jrnls.total / jrnls.per_page)

    return render_template('jrnl_list.html', jrnls=jrnls, total_pages=total_pages)
