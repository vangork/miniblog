from flask import render_template, g, url_for, redirect, session, flash, request, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from datetime import datetime, timedelta
from azure.servicebus import Message
import hashlib
import base64
import uuid
import json
from miniblog import app, db, lm, bus_service
from .forms import RegForm, LoginForm, PostForm, ProfileForm, ForgetForm, ResetForm
from .models import User, Post, Like
from config import POSTS_PER_PAGE,AZURE_SERVICE_BUS_QUEUE

def encryption(data):
    return hashlib.sha224(data.encode('utf8')).hexdigest()

def flash_success(data):
    flash(data, 'success')

def flash_error(data):
    flash(data, 'danger')

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    #if 'user' in session:
    #    g.user = session['user']
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        #db.session.add(g.user)
        db.session.commit()
        #g.search_form = SearchForm()
    #g.locale = get_locale()


#@app.after_request
#def after_request(response):
#    for query in get_debug_queries():
#        if query.duration >= DATABASE_QUERY_TIMEOUT:
#            app.logger.warning(
#                "SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" %
#                (query.statement, query.parameters, query.duration,
#                 query.context))
#    return response


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title = '404'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    message = ['Server Error: {0}'.format(error),
        'Page with issue: {0}'.format(request.path), 'Request Method: {0}'.format(request.method),
        'Request Host: {0}'.format(request.host), 'Login: {0}'.format(g.user.account),
        'Time Stamp: {0} UTC'.format(datetime.utcnow())]
    message = json.dumps(message)
    msg = Message(message.encode('utf-8'), custom_properties={'alert_email_type':1})
    bus_service.send_queue_message(AZURE_SERVICE_BUS_QUEUE, msg)
    return render_template('500.html', title = '500'), 500

@app.route('/', methods = ['GET', 'POST'])
@app.route('/<int:page>', methods=['GET', 'POST'])
def index(page = 1):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
        db.session.add(post)
        db.session.commit()
        flash_success('Post successfully.')
        return redirect(url_for('index'))
    posts = None
    if g.user is not None and g.user.is_authenticated:
        posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template("index.html", title = 'Home', form = form, posts = posts)

@app.route('/reg', methods = ['GET', 'POST'])
def reg():
    if g.user is not None and g.user.is_authenticated:
        flash_error('Log out first to proceed.')
        return redirect(url_for('index'))
    form = RegForm()
    if form.validate_on_submit():
        account = form.username.data
        nickname = form.nickname.data
        email = form.email.data
        password = encryption(form.password.data)
        user = User(account, nickname, email, password, datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=False)
        flash_success('Sign up successfully.')
        return redirect(url_for('index'))
    return render_template('reg.html', title = 'Sign up', form = form)

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    form.username.data = g.user.account
    if request.method == 'GET':
        form.nickname.data = g.user.nickname
        form.email.data = g.user.email
    if form.validate_on_submit():
        nickname = form.nickname.data
        email = form.email.data
        password = encryption(form.password.data)
        password_new = form.password_new.data
        if not password_new and g.user.nickname == nickname and g.user.email == email:
            flash_error('Profile is not changing.')
        else:
            user =  User.verify(g.user.account, password)
            if not user:
                flash_error('Invalid password.')
            else:
                if password_new:
                    user.password = encryption(password_new)
                user.nickname = nickname
                user.email = email
                db.session.commit()
                flash_success('Profile changed successfully.')
                return redirect(url_for('user', username = g.user.account))
    return render_template('profile.html', title = 'Profile', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        flash_error('Log out first to proceed.')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        account = form.username.data
        password = encryption(form.password.data)
        user =  User.verify(account, password)
        if not user:
            flash_error('Invalid account or password.')
        else:
            login_user(user, remember = form.remember_me.data)
            flash_success('Log in successfully.')
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', title = 'Log in', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash_success('Log out successfully.');
    return redirect(url_for('index'))

@app.route('/user/<username>')
@app.route('/user/<username>/<int:page>')
@login_required
def user(username, page=1):
    user = User.query.filter_by(account=username).first()
    if user is None:
        flash_error('User {0} not found.'.format(username))
        return redirect(url_for('index'))
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html', title = 'User', user=user, posts=posts)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post is None:
        flash_error('Post not found.')
        return redirect(url_for('index'))
    if post.author.id != g.user.id:
        flash_error('No permission to delete this post.')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash_success('Delete successfully.')
    return redirect(url_for('user', username=g.user.account))

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(account=username).first()
    if user is None:
        flash_error('User %s not found.' % username)
        return redirect(url_for('index'))
    if user == g.user:
        flash_error('You can\'t follow yourself!')
        return redirect(url_for('user', username=username))
    u = g.user.follow(user)
    if u is None:
        flash_error('Cannot follow {0}.'.format(username))
        return redirect(url_for('user', username=username))
    db.session.add(u)
    db.session.commit()
    flash_success('Follow {0} successfully.'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(account=username).first()
    if user is None:
        flash_error('User %s not found.' % username)
        return redirect(url_for('index'))
    if user == g.user:
        flash_error("You can't unfollow yourself.")
        return redirect(url_for('user', username=username))
    u = g.user.unfollow(user)
    if u is None:
        flash_error('Cannot unfollow {0}.'.format(username))
        return redirect(url_for('user', username=username))
    db.session.add(u)
    db.session.commit()
    flash_success('Unfollo {0} successfully.'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/like/<postid>')
@login_required
def like(postid):
    post = Post.query.filter_by(id = postid).first()
    if post is None:
        #flash_error('Post %s not found.' % postid)
        return jsonify()
    if post.is_liked_by(g.user.id):
        #flash_error('You have already liked this post.')
        return jsonify()
    like = Like(post.id, g.user.id, datetime.utcnow())
    db.session.add(like)
    db.session.commit()
    #flash_success('Like post {0} successfully.'.format(postid))
    return jsonify({'number':post.likes.count()})

@app.route('/unlike/<postid>')
@login_required
def unlike(postid):
    post = Post.query.filter_by(id = postid).first()
    if post is None:
        #flash_error('Post %s not found.' % postid)
        return jsonify()
    if not post.is_liked_by(g.user.id):
        #flash_error("You haven't liked this post.")
        return jsonify()
    like = Like.query.filter_by(post_id = post.id, user_id = g.user.id).first()
    db.session.delete(like)
    db.session.commit()
    #flash_success('Unlike post {0} successfully.'.format(postid))
    return jsonify({'number':post.likes.count()})

@app.route('/forget', methods = ['GET', 'POST'])
def forget():
    form = ForgetForm()
    if form.validate_on_submit():
        email = form.email.data
        user =  User.verify_email(email)
        if not user:
            flash_error("Email doesn't exist.")
        else:
            r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
            user.secret_key = r_uuid.decode('ascii')
            user.secret_key_expiration_time = datetime.utcnow() + timedelta(minutes = 30)
            db.session.commit()
            message = {'reset_username':user.account, 'reset_secret_key':user.secret_key, 'reset_email':user.email, 'reset_host':request.host}
            message = json.dumps(message)
            msg = Message(message.encode('utf-8'), custom_properties={'reset_email_type':1})
            bus_service.send_queue_message(AZURE_SERVICE_BUS_QUEUE, msg)
            flash_success('Successfully sent password reset link to your mailbox.')
            return redirect(url_for('index'))
    return render_template('forget.html', title = 'Forget Password', form = form)

@app.route('/reset/<username>/<uuid>', methods = ['GET', 'POST'])
def reset(username, uuid):
    user = User.verify_secret_key(username, uuid, datetime.utcnow())
    if not user:
        flash_error("Link doesn't exist.")
        return redirect(url_for('index'))
    form = ResetForm()
    form.username.data = user.account
    if form.validate_on_submit():
        user.password = encryption(form.password.data)
        user.secret_key = None
        user.secret_key_expiration_time = None
        db.session.commit()
        flash_success("Successfully reset the password.")
        return redirect(url_for('index'))
    return render_template('reset.html', title = 'Reset password', form = form)

@app.route('/about')
def about():
    return render_template('about.html', title = 'About')

@app.route('/500')
@login_required
def abort500():
    abort(500)
