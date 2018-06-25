#!/usr/bin/env python
# -*- coding:utf-8 -*-
import string
import uuid

from flask import Blueprint, make_response, request
from utils.captcha import Captcha
from io import BytesIO
from utils.dysms_python import demo_sms_send
from .forms import SMSCaptchaForm
from utils import memcaches, restful
import random
from flask import jsonify
import qiniu

common_bp = Blueprint('common', __name__, url_prefix='/c')


@common_bp.route('/')
def index():
    return "这是common首页"


# 图形验证码API
@common_bp.route('/captcha/')
def get_captcha():
    text, image = Captcha.gene_graph_captcha()
    memcaches.set(text.lower(), text.lower())
    out = BytesIO()
    image.save(out, 'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    return resp


# 阿里大于短信测试
@common_bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    __business_id = uuid.uuid1()
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data
        num = string.digits
        captcha = ''.join(random.sample(num, 4))
        # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
        params = {"code":captcha,"product":"test"}
        if demo_sms_send.send_sms(__business_id, "18986205506", "泡泡茶壶", "SMS_122284746", params):
            memcaches.set(telephone, captcha)
            return restful.success()
        else:
            return restful.params_error(message="短信验证码发送失败!")
    else:
        return restful.params_error(message="参数错误!")


# 七牛云api
@common_bp.route('/uptoken/')
def uptoken():
    access_key = 'aRmJChaijJ9RHzlIFNWThFx19lWaTf4IiLdg2eQu'
    secret_key = 'iZOH8pJqJ3jssJmg2Eewv2y-dLFrx7CeMEIPhMmj'
    q = qiniu.Auth(access_key, secret_key)

    bucket = 'zcbbs'
    token = q.upload_token(bucket)
    return jsonify({'uptoken': token})



