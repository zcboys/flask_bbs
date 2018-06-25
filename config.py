#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

DEBUG = True
CSRF_ENABLE = True

SECRET_KEY = os.urandom(24)

# 数据配置信息
USERNAME = '****'
PASSWORD = '******'
HOST = '*****'
PORT = '3306'
DATABASE = 'zcbbs'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False

CMS_USER_ID = 'fegregregre'
FRONT_USER_ID = 'vfdvfdbgfb'

# 邮箱配置信息
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = '278989502@qq.com'
MAIL_PASSWORD = 'oiompnsslccnbgcf'
MAIL_DEFAULT_SENDER = '278989502@qq.com'

# celery配置信息
CELERY_RESULT_BACKEND = 'redis://IP:6379/1'
CELERY_BROKER_URL = 'redis://IP:6379/1'

# ueditor存储路径
# UEDITOR_UPLOAD_PATH 规定本地路径
# UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'images')

# 下面的规定七牛云存储路径
UEDITOR_UPLOAD_PATH = ''
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "*****************"
UEDITOR_QINIU_SECRET_KEY = "****************"
UEDITOR_QINIU_BUCKET_NAME = "zcbbs"
UEDITOR_QINIU_DOMAIN = "http://p6lvi6nq8.bkt.clouddn.com/"

# 每页展示帖子数，设置每页显示10个帖子
PER_PAGE = 10

