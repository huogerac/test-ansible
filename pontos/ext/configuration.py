import os
from importlib import import_module

EXTENSIONS = [
    "pontos.ext.database",
    "pontos.ext.admin",
]


def init_app(app):
    config = get_config_from_env()
    app.config.from_object(config)


def get_config_from_env():
    envname = os.getenv("FLASK_ENV", "development").lower()
    if envname == "production":
        return ProductionConfig()
    if envname == "testing":
        return TestingConfig()
    return DevelopmentConfig()


class ProductionConfig:  # pylint: disable=R0903
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "Ch@nG3_th1s_IN_PR0D!")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://pontos:pontos@localhost/pontos")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ext.admin
    FLASK_ADMIN_SWATCH = "flatly"

    BASIC_AUTH_USERNAME = "pontos"
    BASIC_AUTH_PASSWORD = "pontos"

    # PROGRAMA DE PONTOS
    QTD_PONTOS_PARA_RESGATE = int(os.getenv("QTD_PONTOS_PARA_RESGATE", "10"))


class TestingConfig(ProductionConfig):  # pylint: disable=R0903
    FLASK_ENV = "testing"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "postgresql://pontos:pontos@localhost/pontos_test")


class DevelopmentConfig(ProductionConfig):  # pylint: disable=R0903
    FLASK_ENV = "development"
    DEBUG = True


def load_extensions(app):
    for extension in EXTENSIONS:
        mod = import_module(extension)
        print("  ...loading {}".format(extension))
        mod.init_app(app)
