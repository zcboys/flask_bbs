#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint, views, render_template, request, session, g, abort
from sqlalchemy import func

from .forms import FrontSignupFrom, FrontSigninForm, AddPostForm, AddCommentForm, EditPostForm
from .models import FrontUserModel
from exts import db
from utils import restful, safeutils
import config
from ..models import BannerModel, BoardModel, CommentModel
from .decorators import login_required
from ..models import PostModel, HighlightPostModel
from flask_paginate import Pagination, get_page_parameter
from sqlalchemy import or_

front_bp = Blueprint('front', __name__)


@front_bp.route('/')
def index():
    q = request.args.get("q")
    board_id = request.args.get("bd", type=int, default=None)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(5)
    boards = BoardModel.query.all()
    sort = request.args.get("st", type=int, default=1)
    # posts = PostModel.query.all()
    page = request.args.get(get_page_parameter(),type=int, default=1)
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE

    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        # 按照加精的时间倒序排序
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc(), PostModel.create_time.desc())
    elif sort == 3:
        # 按照点赞的数量排序
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        # 按照评论的数量排序
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(
            func.count(CommentModel.id).desc(), PostModel.create_time.desc())

    if q:
        posts = PostModel.query.filter(or_(PostModel.title.contains(q))).order_by('-create_time').slice(start, end)
        total = query_obj.filter(or_(PostModel.title.contains(q))).count()
    else:
        if board_id:
            query_obj = query_obj.filter(board_id == board_id)
            posts = query_obj.slice(start, end)
            total = query_obj.count()
        else:
            posts = query_obj.slice(start, end)
            total = query_obj.count()
    
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort
    }
    return render_template('front/front_index.html', **context)


# 注册视图
class FrontSignupView(views.MethodView):
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template('front/front_signup.html', return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = FrontSignupFrom(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUserModel(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_errors())


front_bp.add_url_rule('/front_signup/', view_func=FrontSignupView.as_view('front_signup'))


class FrontSigninView(views.MethodView):
    def get(self):
        return render_template('front/front_signin.html')

    def post(self):
        form = FrontSigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remember.data
            user = FrontUserModel.query.filter_by(telephone=telephone).first()
            if user and user.check_pwd(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message="手机号或者密码错误!")
        else:
            return restful.params_error(message=form.get_errors())


front_bp.add_url_rule('/front_signin/', view_func=FrontSigninView.as_view('front_signin'))


# 编辑帖子页面视图
@front_bp.route('/apost/', methods=['GET', 'POST'])
@login_required
def apost():
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template('front/front_apost.html', boards=boards)
    else:
        form = AddPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message="没有这个板块!")
            post = PostModel(title=title, content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_errors())


# 帖子详情页
@front_bp.route('/p/<post_id>')
def post_detail(post_id):
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    context = {
        'post': post
    }
    return render_template('front/front_pdetail.html', **context)

# 帖子内容编辑
@front_bp.route('/p/<post_id>/edit/', methods=['GET', 'POST'])
@login_required
def post_edit(post_id):
    if request.method == 'GET':
        post = PostModel.query.get(post_id)
        boards = BoardModel.query.all()
        return render_template('front/front_post_edit.html', post=post, boards=boards)
    else:
        form = EditPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message="没有这个板块!")
            post = PostModel.query.get(post_id)
            post.board = board
            post.title = title
            post.content = content
            post.author = g.front_user
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_errors())


# 添加评论
@front_bp.route('/acomment/', methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这篇文章!")
    else:
        return restful.params_error(message=form.get_errors())

