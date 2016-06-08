# -*- coding=utf-8 -*-
from flask import render_template, flash, redirect, url_for, request, current_app
from flask.ext.login import login_required, current_user, login_user, logout_user
from forms import LoginForm, RegistrationForm, PostArticleForm, PostCategoryForm
from sqlalchemy import desc
from . import admin
from ..models import User, Article, Category
from .. import db


@admin.route('/')
def index():
    return render_template('admin/index.html')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(request.args.get('next') or url_for('admin.index'))
        flash(u'用户密码不正确')
    return render_template('admin/login.html', form=form)


@admin.route('/register', methods=['GET', 'POST'])
def register():
    app = current_app._get_current_object()
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.registerkey.data != app.config['USER_REGISTER_CODE']:
            flash(u'注册码不符,请返回重试.')
            return redirect(url_for('admin.register'))
        else:
            if form.password.data != form.password2.data:
                flash(u'两次输入密码不一')
                return redirect(url_for('admin.register'))
            else:
                user = User(username=form.username.data, password=form.password.data, real_name=form.real_name.data)
                db.session.add(user)
                flash(u'您已经注册成功')
                return redirect(url_for('admin.login'))
    return render_template('admin/register.html', form=form)


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已经登出了系统')
    return redirect(url_for('main.index'))


@admin.route('/article', methods=['GET', 'POST'])
@login_required
def article():
    form = PostArticleForm()
    if request.method == 'POST':
        if form.title.data != '' and form.body.data != '' and form.category_id.data.id != '':
            acticle = Article(title=form.title.data, body=form.body.data, category_id=str(form.category_id.data.id),
                              user_id=current_user.id)
            db.session.add(acticle)
            return u'1'
        else:
            return u'0'
    return render_template('admin/article.html', form=form)


@admin.route('/article/control')
@admin.route('/article/control/<int:page>')
@login_required
def article_control(page=1):
    pages = Article.query.order_by(desc(Article.create_time)).paginate(page, 10, False)
    list = pages.items
    return render_template('admin/control.html', list=list, pages=pages)


@admin.route('/article/edit/<int:id>', methods=['POST','GET'])
@login_required
def article_edit(id):
    form = PostArticleForm()
    article = Article.query.get_or_404(id)
    if request.method == 'POST':
        article.title = form.title.data
        article.body = form.body.data
        article.category_id = form.category_id.data.id
        try:
            db.session.add(article)
            return u'1'
        expect:
            db.session.rollback()
            return u'0'
    flash(u'您当前修改的是'+str(article.id)+u'编号的主题')
    return render_template('admin/edit.html', article=article, form=form)


@admin.route('/article/del', methods=['GET'])
@login_required
def article_del():
    if request.args.get('id') is not None and request.args.get('a') == 'del':
        x = Article.query.filter_by(id=request.args.get('id')).first()
        if x is not None:
            db.session.delete(x)
            db.session.commit()
            flash(u'已经删除' + x.title)
            return redirect(url_for('admin.article_control'))
        flash(u'请检查输入')
        return redirect(url_for('admin.article_control'))


@admin.route('/category', methods=['GET', 'POST'])
def category():
    clist = Category.query.all()
    form = PostCategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        flash(u'分类添加成功')
        return redirect(url_for('admin.index'))
    return render_template('admin/category.html', form=form, list=clist)


@admin.route('/category/del', methods=['GET'])
@login_required
def category_del():
    if request.args.get('id') is not None and request.args.get('a') == 'del':
        x = Category.query.filter_by(id=request.args.get('id')).first()
        if x is not None:
            db.session.delete(x)
            db.session.commit()
            flash(u'已经删除' + x.name)
            return redirect(url_for('admin.category'))
        flash(u'请检查输入')
        return redirect(url_for('admin.category'))
