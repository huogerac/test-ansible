from flask import Flask
import connexion

from pontos.exceptions import NotFoundException, InvalidValueException, UnauthorizedException


def create_api_app(version="/api"):
    app = Flask(__name__)
    connexion_app = connexion.FlaskApp(__name__, specification_dir="../api/")
    connexion_app.add_api("openapi.yaml", validate_responses=True, base_path=version)
    app = connexion_app.app

    @app.errorhandler(NotFoundException)
    def not_found_handler(error):  # pylint: disable=W0612
        return {
            "detail": str(error),
            "status": 404,
            "title": "Not Found",
        }

    @app.errorhandler(InvalidValueException)
    def invalid_value_handler(error):  # pylint: disable=W0612
        return {
            "detail": str(error),
            "status": 400,
            "title": "Bad Request",
        }

    @app.errorhandler(UnauthorizedException)
    def unauthorized_handler(error):  # pylint: disable=W0612
        return {
            "detail": str(error),
            "status": 401,
            "title": "Unauthorized Request",
        }

    return app
