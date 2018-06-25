#!/usr/bin/env python
# -*- coding:utf-8 -*-

from .views import front_bp
import config
from flask import session, g, render_template
from .models import FrontUserModel


@front_bp.before_request
def before_request():
    if config.FRONT_USER_ID in session:
        front_user_id = session.get(config.FRONT_USER_ID)
        front_user = FrontUserModel.query.get(front_user_id)
        if front_user:
            g.front_user = front_user


@front_bp.errorhandler
def page_not_fount():
    return render_template('front/404.html')