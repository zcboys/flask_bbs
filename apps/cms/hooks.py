#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import session, g

from apps.cms.models import CmsUserModel
from .views import cms_bp
import config


@cms_bp.before_request
def before_request():
    if config.CMS_USER_ID in session:
        user_id = session.get(config.CMS_USER_ID)
        user = CmsUserModel.query.get(user_id)
        if user:
            g.cms_user = user

