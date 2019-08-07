import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'e2a87a53bf8ea2b8cfd7fd1f80c70896'
    MAX_STORAGE_TIME = os.environ.get('MAX_STORAGE_TIME') or 1440
    MAIL_SENDER = os.environ.get('MAIL_SENDER') or 'url_shortener@url_shortener.com'
    ADMIN_EMAIL = os.environ.get('MAIL_SENDER') or None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or None
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or None
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def init_app(cls, app):
        pass

class DevelopmentConfig(Config):
    """Development config, only for dev purposes."""
    REDISTOGO_URL = 'redis://localhost:6379'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static/site.db'
    DEBUG = True

class TestingConfig(Config):
    """Testing config for unit tests"""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///static/site-test.db'
    TESTING = True

class ProductionConfig(Config):
    """App configuration for production."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
        if getattr(cls, 'MAIL_USE_TLS', None):
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.ADMIN_EMAIL],
            subject='URL Shortener ERROR',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class HerokuConfig(ProductionConfig):
    """App configuration for deploying on Heroku Platform"""
    REDISTOGO_URL = os.environ.get('REDISTOGO_URL') or 'redis://localhost:6379'

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


config = {
    'dev_config': DevelopmentConfig(),
    'prod_config': ProductionConfig(),
    'heroku_config': HerokuConfig(),
    'testing': TestingConfig(),
    'default': DevelopmentConfig()
    }