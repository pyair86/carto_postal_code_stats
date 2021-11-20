from App.main import app


def test_status_200():
    response = app.test_client().get("/")
    assert response.status_code == 200


def test_status_404():
    response = app.test_client().get("/postal_codesssss/")
    assert response.status_code == 404


def test_status_302():
    response = app.test_client().get("/postal_codes/")
    assert response.status_code == 302
