# -*- coding=utf-8 -*-
from flask import render_template, redirect, url_for, flash, request, current_app
from . import main
from ..models import Article
from sqlalchemy import desc


@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
@main.route('/index/<int:page>', methods=['GET'])
def index(page=1):
    app = current_app._get_current_object()
    posts = Article.query.order_by(desc(Article.create_time)).paginate(page, app.config['POSTS_PER_PAGE'], False).items
    return render_template('index.html', list=posts)


@main.route('/read/', methods=['GET'])
def read():
    a = Article.query.filter_by(id=request.args.get('id')).first()
    if a is not None:
        return render_template('read.html', a=a)
    flash(u'未找到相关文章')
    return redirect(url_for('main.index'))
