from flask import Flask
from apps.cms import cms_bp
from apps.common import common_bp
from apps.front import front_bp
from apps.ueditor import bp as ueditor_bp
from exts import db, mail
import config
from flask_wtf import CSRFProtect
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(cms_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)
    app.register_blueprint(ueditor_bp)
    db.init_app(app)
    mail.init_app(app)
    CSRFProtect(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
