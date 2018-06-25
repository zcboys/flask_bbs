#!/usr/bin/env python
# -*- coding:utf-8 -*-


from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from zcbbs import create_app
from apps.cms.models import CmsUserModel
from apps.front.models import FrontUserModel
from apps.models import BannerModel, BoardModel, PostModel, CommentModel, HighlightPostModel

app = create_app()

manager = Manager(app)

Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-e', '--email', dest='email')
@manager.option('-p', '--password', dest='password')
def create_cms_user(username, email, password):
    cms_user = CmsUserModel(username=username, email=email, password=password)
    db.session.add(cms_user)
    db.session.commit()
    print("cms用户%s添加成功!" % cms_user.username)


@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUserModel(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print("前台用户%s创建成功!" % user.username)


# 测试帖子创建
@manager.command
def create_test_post():
    for x in range(1,255):
        title = "标题%s" % x
        content = "内容%s" % x
        board = BoardModel.query.first()
        author = FrontUserModel.query.first()
        post = PostModel(title=title, content=content)
        post.board = board
        post.author = author
        db.session.add(post)
        db.session.commit()
    print("测试帖子添加成功!")


if __name__ == "__main__":
    manager.run()