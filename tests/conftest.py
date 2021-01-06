import os
import pytest

from pontos.app import create_app


@pytest.fixture(scope="session")
def app():
    os.environ["FLASK_ENV"] = "production"
    app = create_app()
    with app.app_context():
        yield app
