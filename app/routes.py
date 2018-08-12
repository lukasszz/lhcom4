from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, JrnlForm
from app.models import User, Jrnl
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html', title='Home', user=current_user, jrnls=Jrnl.get_news())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/jrnl_ed', methods=['POST', 'GET'])
@login_required
def jrnl_ed():
    form = JrnlForm()
    if form.validate_on_submit():
        jrnl = Jrnl(body=form.jrnl.data, author=current_user)
        db.session.add(jrnl)
        db.session.commit()
        flash('Added new Jrnl entry!')
        return redirect(url_for('index'))
    return render_template('jrnl_ed.html', form=form)
