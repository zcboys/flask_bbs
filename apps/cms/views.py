#!/usr/bin/env python
# -*- coding:utf-8 -*-


from flask import (
    Blueprint,
    render_template,
    views, request,
    session,
    redirect,
    url_for,
    g
)
from flask_mail import Message

from .forms import LoginFrom, ResetpwdForm, ResetEmailForm, AddBoardForm, UpdateBoardForm
from .models import CmsUserModel
import config
from .decorators import login_required
from exts import db, mail
from utils import restful
import string, random
from tasks import send_mail
from utils import memcaches
from ..models import BannerModel, BoardModel, HighlightPostModel, PostModel
from apps.cms.forms import AddBannerForm, UpdateBannerFrom
from sqlalchemy import or_
from flask_paginate import Pagination, get_page_parameter


cms_bp = Blueprint('cms', __name__, url_prefix='/cms')


# 首页视图
@cms_bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


# 注销视图
@cms_bp.route('/logout/')
@login_required
def logout():
    return redirect(url_for('cms.login'))


# 个人信息页视图
@cms_bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


# 修改密码视图
class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            newpwd = form.newpwd2.data
            cms_user = g.cms_user
            if cms_user:
                cms_user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error(message="用户不存在!")
        else:
            return restful.params_error(message=form.get_errors())


cms_bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            email1 = CmsUserModel.query.filter_by(email=email).first()
            if email1:
                return restful.params_error(message="该邮箱已被注册!")
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_errors())


# 发送邮箱验证码视图
@cms_bp.route('/email_captcha/')
def email_captcha():
    # form = EmailCaptchaForm(request.form)
    # print(form.email.data)
    # if form.validate():
    # email = form.email.data
    email = request.args.get('email')
    if not email and email == None:
        return restful.params_error(message="邮箱不能为空!")
    if email == g.cms_user.email:
        return restful.params_error(message="新邮箱不能与原邮箱一样!")
    source = list(string.ascii_letters+string.digits)
    captcha = ''.join(random.sample(source, 6))
    # message = Message('zcbbs邮箱验证码', recipients=[email], body="您的邮箱验证码为：%s" % captcha)
    # try:
    #     mail.send(message)
    # except:
    #     return restful.server_error()
    # return restful.success()
    send_mail.delay('bbs论坛邮箱验证码', [email], '您的邮箱验证码为:%s' % captcha)
    memcaches.set(email, captcha)
    return restful.success()


# 发送邮箱验证码测试API
@cms_bp.route('/email/')
def email():
    message = Message('测试邮件', recipients=['278989502@qq.com'], body='测试')
    mail.send(message)
    return '邮件发送成功!'


cms_bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))


# 登录视图
class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginFrom(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            cms_user = CmsUserModel.query.filter_by(email=email).first()
            if cms_user and cms_user.check_password(password):
                session[config.CMS_USER_ID] = cms_user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message="邮箱不存在!")
        else:
            return self.get(message=form.get_errors())


cms_bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))


# 轮播图
@cms_bp.route('/banners/')
@login_required
def banners():
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


# 添加轮播图
@cms_bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_errors())


# 更新轮播图
@cms_bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerFrom(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message="没有这个轮播图!")
    else:
        return restful.params_error(message=form.get_errors())


# 删除轮播图
@cms_bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message="请传入轮播图ID!")
    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message="没有这个轮播图!")
    db.session.delete(banner)
    db.session.commit()
    return restful.success()


# 板块视图
@cms_bp.route('/boards/')
@login_required
def boards():
    board_models = BoardModel.query.all()
    context= {
        'boards':board_models
    }
    return render_template('cms/cms_boards.html', **context)


# 添加板块
@cms_bp.route('/aboard/', methods=['POST'])
@login_required
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_errors())


# 编辑更新板块
@cms_bp.route('/uboard/', methods=['POST'])
@login_required
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if not board:
            return restful.params_error(message="板块不存在!")
        board.name = name
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_errors())


@cms_bp.route('/dboard/', methods=['POST'])
@login_required
def dboard():
    board_id = request.form.get("board_id")
    print(board_id)
    if not board_id:
        return restful.params_error(message="请传入板块ID!")
    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message="没有这个板块!")
    db.session.delete(board)
    db.session.commit()
    return restful.success()


# 帖子管理
@cms_bp.route('/posts/')
@login_required
def posts():
    q = request.args.get('q')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    # if q:
    #     posts = PostModel.query.filter(or_(PostModel.title.contains(q))).order_by('-create_time')
    # else:
    if q:
        posts = PostModel.query.filter(or_(PostModel.title.contains(q))).order_by('-create_time').slice(start, end)
        total = PostModel.query.filter(or_(PostModel.title.contains(q))).count()
    else:
        posts = PostModel.query.slice(start, end)
        total = PostModel.query.count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    content = {
        'posts': posts,
        'pagination': pagination,
    }
    return render_template('cms/cms_posts.html', **content)


# 帖子加精
@cms_bp.route('/hpost/', methods=['POST'])
@login_required
def hpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message="请传入帖子ID!")
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(message="没有这篇帖子!")
    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()


# 帖子取消加精
@cms_bp.route('/uhpost/', methods=['POST'])
@login_required
def uhpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message="请传入帖子ID!")
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(message="没有这篇帖子!")
    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


# 删除帖子
@cms_bp.route('/dpost/', methods=['POST'])
@login_required
def dpost():
    post_id = request.form.get('post_id')
    if not post_id:
        return restful.params_error(message="请传入帖子ID!")
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error(message="没有这篇帖子!")
    db.session.delete(post)
    db.session.commit()
    return restful.success()
