from miniblog import db
from miniblog import app
from sqlalchemy import or_, and_

followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(32), index=True, unique=True)
    nickname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    creation_time = db.Column(db.DateTime, index=True)
    last_seen = db.Column(db.DateTime)
    secret_key = db.Column(db.String(100))
    secret_key_expiration_time = db.Column(db.DateTime)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User',
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic')

    def __init__(self, account, nickname, email, password, creation_time):
        self.account = account
        self.nickname = nickname
        self.email = email
        self.password = password
        self.creation_time = creation_time


    @staticmethod
    def exist(username):
        if User.query.filter_by(account=username).first() is None:
            return False
        else:
            return True

    @staticmethod
    def verify_email(email):
        user = User.query.filter_by(email=email).first() 
        if user is None:
            return False
        else:
            return user

    @staticmethod
    def verify_secret_key(useraccount, uuid, time):
        user = User.query.filter(and_(User.account == useraccount, User.secret_key==uuid, User.secret_key_expiration_time>time)).first() 
        if user is None:
            return False
        else:
            return user
    
    @staticmethod
    def verify(username, password):
        user = User.query.filter_by(account=username).first()
        if user is None:
            return False
        elif user.password != password:
             return False
        else:
            return user
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(
                followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())

    def __repr__(self):  # pragma: no cover
        return '<User %r>' % (self.account)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    likes = db.relationship('Like', backref='post', lazy='dynamic')    

    def is_liked_by(self, userid):
        return self.likes.filter(Like.user_id == userid).count() > 0

    def __repr__(self):  # pragma: no cover
        return '<Post %r>' % (self.body)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime)
    def __init__(self, postid, userid, timestamp):
        self.post_id = postid
        self.user_id = userid
        self.timestamp = timestamp

    def __repr__(self):  # pragma: no cover
        return '<Like %r>' % (self.id)