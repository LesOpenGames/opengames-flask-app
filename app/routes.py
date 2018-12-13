from flask import render_template, flash, redirect, url_for, request, g
from werkzeug.urls import url_parse
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
from flask_babel import _, get_locale

from app import app, db
from app.forms import LoginForm, RegisterForm, EditProfileForm, PostForm
from app.forms import  ResetPasswordRequestForm,  ResetPasswordForm
from app.models import User, Post
from app.email import send_password_reset_email

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        flash(_('sorry, you cant reset passwd while connected'))
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash(_('token not verified'))
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(user.username+': Password resetted to '+form.password.data)
        flash(_('For User: %(username) Password resetted to: %(passwrord) ', username=user.username, passwrord=form.pasword.data))
        return redirect(url_for('login'))
    return render_template('reset_password.html', title='Password Reset', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash( _('Email sent for password reset'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash( _('Post published'))
        return redirect(url_for('index'))
    page_num = request.args.get('page_num', 1, type=int)
    posts = current_user.followed_posts().paginate(
            page_num, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page_num=posts.next_num)\
            if posts.has_next else None
    prev_url = url_for('index', page_num=posts.prev_num)\
            if posts.has_prev else None
    return  render_template('index.html', title='Home Page', form=form, posts=posts.items,
            next_url=next_url, prev_url=prev_url)

@app.route('/explore', methods=['GET', 'POST'])
def explore():
    page_num = request.args.get('page_num', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
            page_num, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page_num=posts.next_num)\
            if posts.has_next else None
    prev_url = url_for('explore', page_num=posts.prev_num)\
            if posts.has_prev else None
    return  render_template('index.html', title='Explore', posts=posts.items,
            next_url=next_url, prev_url=prev_url)

@app.route('/notitle')
def notitle():
    return  render_template('index.html')

@app.route('/posts')
@login_required
def posts():
    all_users = User.query.all()
    posts = []
    for u in all_users:
        posts.append( { 'author': u, 'body': 'This is my body' })
    return render_template('posts.html', title='All Posts', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash( _('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        # next page is from outside or None
        if not next_page or url_parse(next_page).netloc != '':
            next_page=url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        #if user is None or not user.check_password(form.password.data):
        flash(_('Congratulation %(username), you are registered', username=user.username))
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page_num = request.args.get('page_num', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
            page_num, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page_num=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page_num=posts.prev_num) \
        if posts.has_prev else None
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Sucessfully updated your profile'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='User Profile', form=form)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash( _('User %(username) not found', username=username))
        return redirect(url_for('index'))
    if user == current_user.username:
        flash( _('Cannot follow yourself'))
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash( _('You are following %(username)', username=username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash( _('User %(username) not found', username=username))
        return redirect(url_for('index'))
    if user == current_user.username:
        flash( _('Cannot unfollow yourself'))
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash( _('You have unfollowed %(username)', username=username))
    return redirect(url_for('user', username=username))
