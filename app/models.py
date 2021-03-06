# -*- coding=utf-8 -*-
from . import db, login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash  # 引入密码加密 验证方法
from flask.ext.login import UserMixin  # 引入flask-login用户模型继承类方法


class Pageabout(db.Model):
    __tablename__ = 'pageabouts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    menu = db.Column(db.String(32), unique=True)
    about = db.Column(db.Text)
    create_time = db.Column(db.DATETIME, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    body = db.Column(db.Text)
    create_time = db.Column(db.DATETIME, default=datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    articles = db.relationship('Article', backref='category')


class User(UserMixin, db.Model):
    # 在使用Flask-Login作为登入功能时,在user模型要继承UserMimix类.
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    real_name = db.Column(db.String(64), unique=True)
    articles = db.relationship('Article', backref='user')
    pageabouts = db.relationship('Pageabout', backref='user')

    @property
    def password(self):
        raise AttributeError(u'密码属性不正确')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        # 增加password会通过generate_password_hash方法来加密储存

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        # 在登入时,我们需要验证明文密码是否和加密密码所吻合


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
