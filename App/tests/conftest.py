from App.main import app as flask_app
import pytest


@pytest.fixture
def app():
    flask_app.testing = True
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()