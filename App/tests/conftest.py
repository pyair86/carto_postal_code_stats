from App.main import app as flask_app
import pytest


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def client():
    app = flask_app
    app.config['TESTING'] = True

    with app.app_context():
        with app.test_client() as client:
            yield client




