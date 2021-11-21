from App.tests.conftest import flask_app
import json


def test_postal_codes():

    flask_app.config['TESTING'] = True

    with open("App/tests/all_polygons.json") as all_polygons_json:
        all_polygons_response = json.load(all_polygons_json)

        response = flask_app.test_client().get("/postal_codes/")
        assert response.get_json() == all_polygons_response

        response = flask_app.test_client().get("/postal_codes_agg/")
        assert response.get_json() != all_polygons_response


def test_status_200():
    response = flask_app.test_client().get("/")
    text_response = response.get_data(as_text=True)
    assert "CARTO" in text_response
    assert response.status_code == 200


def test_status_404():
    response = flask_app.test_client().get("/postal_codesssss/")
    assert response.status_code == 404


def test_status_302_redirect_login():
    flask_app.config['TESTING'] = False
    response = flask_app.test_client().get("/postal_codes/28011")
    assert response.status_code == 302



