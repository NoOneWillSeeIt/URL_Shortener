from flask import Flask, request
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from url_shortener.config import config

db = SQLAlchemy()
babel = Babel()

def create_app(config_name='dev_config'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    babel.init_app(app)

    from url_shortener.routes import routes
    app.register_blueprint(routes)

    return app