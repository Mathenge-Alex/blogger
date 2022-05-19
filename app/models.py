from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(200),index = True)
    email = db.Column(db.String(200),unique = True,index = True)
    bio = db.Column(db.String(200))
    profile_pic_path = db.Column(db.String)
    password_hash = db.Column(db.String(200))
    posts = db.relationship('Post',backref='user',lazy='dynamic')
    comment = db.relationship('Comment',backref='user',lazy='dynamic')
    like = db.relationship('Like',backref='user',lazy='dynamic')
    dislike = db.relationship('Dislike',backref='user',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'User {self.username}'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200))
    content = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    time_created = db.Column(db.DateTime(timezone = True), default = datetime.now)
    comment = db.relationship('Comment',backref='post',lazy = 'dynamic')
    like = db.relationship('Like',backref='post',lazy='dynamic')
    dislike = db.relationship('Dislike',backref='post',lazy='dynamic')

    def save_post(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_posts(cls):
        posts = Post.query.all()
        return posts


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String(255))
    time_created = db.Column(db.DateTime(timezone = True), default = datetime.now)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))

    def save_comment(self):
        db.session.add(self)
        db.session.commit()


    @classmethod
    def get_comments(self,id):
        comment = Comment.query.order_by(Comment.time_commented.desc()).filter_by(post_id = id).all()
        return comment

    def __repr__(self):
        return f'comment:{self.comment}'


class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))

    def save_likes(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_likes(cls,id):
        like = Like.query.filter_by(post_id=id).all()
        return like

    def __repr__(self):
        return f'{self.user_id}:{self.post_id}'


class Dislike(db.Model):
    __tablename__ = 'dislikes'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))
    
    def save_dislikes(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_dislikes(cls,id):
        dislike = Dislike.query.filter_by(post_id=id).all()
        return dislike

    def __repr__(self):
        return f'{self.user_id}:{self.post_id}'


class Quote:
    def __init__(self,author,quote):
        self.author = author
        self.quote = quote


class Subscriber(db.Model):
    __tablename__ = 'subscribers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200),unique = True,index = True)

    def save_subscribers(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Subscriber: {self.mail}'