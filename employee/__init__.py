import os
from flask import Flask
from . import db
from .views import auth
from .views import user_center
from .views import blog
from .views import attendance


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'employee.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user_center.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(attendance.bp)
    app.add_url_rule('/', endpoint='index')

    return app
