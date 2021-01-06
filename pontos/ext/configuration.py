import os
from importlib import import_module

EXTENSIONS = []


def init_app(app):
    config = get_config_from_env()
    app.config.from_object(config)


def get_config_from_env():
    envname = os.getenv("FLASK_ENV", "development").lower()
    if envname == "production":
        return ProductionConfig()
    return DevelopmentConfig()


class ProductionConfig(object):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "Ch@nG3_th1s_IN_PR0D!")


class DevelopmentConfig(ProductionConfig):
    FLASK_ENV = "development"
    DEBUG = True


def load_extensions(app):
    for extension in EXTENSIONS:
        mod = import_module(extension)
        print("  ...loading {}".format(extension))
        mod.init_app(app)
