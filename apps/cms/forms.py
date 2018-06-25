#!/usr/bin/env python
# -*- coding:utf-8 -*-

from apps.forms import BaseForm
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo, ValidationError
from flask import g
from utils import memcaches


class LoginFrom(BaseForm):
    email = StringField(validators=[Email(message="请输入正确格式的邮箱地址!"), InputRequired(message="请输入邮箱地址!")])
    password = StringField(validators=[Length(5, 20, message="密码长度为5-20个字符!"), InputRequired(message="请输入密码!")])
    remember = BooleanField()


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(5, 20, message='请输入正确格式的旧密码'), InputRequired(message="请输入旧密码!")])
    newpwd1 = StringField(validators=[Length(5, 20, message='请输入正确格式的新密码'), InputRequired(message="新密码不能为空!")])
    newpwd2 = StringField(validators=[EqualTo("newpwd1", message='确认密码必须和新密码保持一致'), InputRequired(message="请再次输入密码!!")])

    def validate_oldpwd(self, filed):
        self.oldpwd = filed.data
        cms_user = g.cms_user
        if not cms_user.check_password(self.oldpwd):
            raise ValidationError("旧密码不正确!")

    def validate_newpwd1(self, filed):
        self.newpwd1 = filed.data
        if self.newpwd1 == self.oldpwd:
            raise ValidationError("新密码不能与旧密码一样!")


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message="请输入正确格式的邮箱地址!")])
    captcha = StringField(validators=[Length(min=6, max=6, message="请输入正确长度的验证码!")])

    def validate_captcha(self, filed):
        captcha = filed.data
        email = self.email.data
        captcha_cache = memcaches.get(email)
        if not captcha_cache or captcha.lower() != captcha_cache.lower():
            raise ValidationError('邮箱验证码错误!')

    def validate_email(self, filed):
        email = filed.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError("不能修改为当前邮箱!")


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入轮播图名称!")])
    image_url = StringField(validators=[InputRequired(message="请输入图片链接!")])
    link_url = StringField(validators=[InputRequired(message="请输入跳转链接!")])
    priority = IntegerField(validators=[InputRequired(message="请输入轮播图的优先级!")])


class UpdateBannerFrom(AddBannerForm):
    banner_id = IntegerField(validators=[InputRequired(message="请输入轮播图的ID")])


class AddBoardForm(BaseForm):
    name = StringField(validators=[InputRequired(message="请输入板块名称!")])


class UpdateBoardForm(AddBoardForm):
    board_id = IntegerField(validators=[InputRequired(message="请输入板块ID!")])


