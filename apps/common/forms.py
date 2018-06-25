#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ..forms import BaseForm
from wtforms import StringField
from wtforms.validators import regexp, InputRequired
import hashlib


class SMSCaptchaForm(BaseForm):
    salt = 'vfewfrefgreg'  # 盐,随便给定一个值
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{13}')])
    sign = StringField(validators=[InputRequired()])  ## 签名

    # 重写验证器
    def validate(self):
        result = super(SMSCaptchaForm, self).validate()
        # 上面的父验证器通过了才执行下面的代码
        if not result:
            return False
        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data

        # md5加密(timestamp+telephone+salt)
        # md5函数必须传一个bytes类型的字符串进去
        sign2 = hashlib.md5((timestamp+telephone+self.salt).encode('utf-8')).hexdigest() # hexdigest 获取md5值的字符串
        if sign == sign2:
            return True
        else:
            return False

