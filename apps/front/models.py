#!/usr/bin/env python
# -*- coding:utf-8 -*-


from ..forms import BaseForm
from exts import db
import shortuuid
import enum
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class GenderEnum(enum.Enum):
    # 男性
    MALE = 1
    # 女性
    FEMALE = 2
    # 秘密
    SECRET = 3
    # 未填写
    UNKNOW = 4


class FrontUserModel(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100), primary_key=True, default=shortuuid.uuid)
    username = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50))
    join_time = db.Column(db.DateTime, default=datetime.now)

    # 真实姓名
    readlname = db.Column(db.String(50))
    # 头像
    avatar = db.Column(db.String(300))
    # 个性签名
    signature = db.Column(db.String(100))
    # 性别， 采用枚举类型
    gender = db.Column(db.Enum(GenderEnum), default=GenderEnum.UNKNOW)

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(FrontUserModel, self).__init__(*args, **kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, input_pwd):
        self._password = generate_password_hash(input_pwd)

    def check_pwd(self, raw_password):
        return check_password_hash(self.password, raw_password)

