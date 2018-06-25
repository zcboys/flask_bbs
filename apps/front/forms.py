#!/usr/bin/env python
# -*- coding:utf-8 -*-


from ..forms import BaseForm
from wtforms.validators import regexp, EqualTo, ValidationError, InputRequired
from wtforms import StringField, BooleanField, IntegerField
from utils import memcaches


class FrontSignupFrom(BaseForm):
    telephone = StringField(validators=[regexp(r"1[345789]\d{9}", message="请输入正确格式的手机号码!")])
    sms_captcha = StringField(validators=[regexp(r"\w{4}", message="请输入正确格式的短信验证码!")])
    username = StringField(validators=[regexp(r".{2,20}", message="用户名长度为2-20的任意字符!")])
    password1 = StringField(validators=[regexp(r"[0-9a-zA-Z_\.]{6,20}", message="密码不包含除了_.的其他特殊字符!")])
    password2 = StringField(validators=[EqualTo("password1", message="两次输入的密码不一致，请重新输入!")])
    graph_captcha = StringField(validators=[regexp(r"\w{4}", message="图形验证码为4个字符!")])

    def validate_sms_captcha(self, field):
        sms_captcha = field.data
        telephone = self.telephone.data

        sms_captcha_mem = memcaches.get(telephone)
        if not sms_captcha_mem or sms_captcha_mem != sms_captcha:
            raise ValidationError(message="短信验证码错误!")

    def validate_graph_captcha(self, field):
        grapt_captcha = field.data
        grapt_captcha_mem = memcaches.get(grapt_captcha.lower())
        if not grapt_captcha_mem:
            raise ValidationError(message="图形验证码错误!")


class FrontSigninForm(BaseForm):
    telephone = StringField(validators=[regexp(r"1[345789]\d{9}", message="请输入正确格式的手机号码!")])
    password = StringField(validators=[regexp(r"[0-9a-zA-Z_\.]{6,20}", message="密码为6-20个字符(包含特殊字符_.)!")])
    remember = BooleanField()


class AddPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message="请传入标题!")])
    content = StringField(validators=[InputRequired(message="请传入内容!")])
    board_id = IntegerField(validators=[InputRequired(message="请传入板块ID")])

class EditPostForm(BaseForm):
    title = StringField(validators=[InputRequired(message="请传入标题!")])
    content = StringField(validators=[InputRequired(message="请传入内容!")])
    board_id = IntegerField(validators=[InputRequired(message="请传入板块ID")])

class AddCommentForm(BaseForm):
    content = StringField(validators=[InputRequired(message="请输入评论内容!")])
    post_id = IntegerField(validators=[InputRequired(message="请输入帖子ID!")])
