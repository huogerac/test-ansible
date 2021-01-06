from flask import Flask
import connexion


def create_api_app(version="api"):
    app = Flask(__name__)
    connexion_app = connexion.FlaskApp(__name__, specification_dir="../api/")
    connexion_app.add_api("openapi.yaml", validate_responses=True, base_path="/api")
    app = connexion_app.app

    return app
