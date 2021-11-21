from App.tests.conftest import flask_app
from App.main import ConfJsonReader
from App.database_py_files.db_connection_manager import DBConnectionManager
from App.database_py_files.db_connector import DBConnector


def test_status_200():
    response = flask_app.test_client().get("/")
    text_response = response.get_data(as_text=True)
    assert "CARTO" in text_response
    assert response.status_code == 200


def test_status_404():
    response = flask_app.test_client().get("/postal_codesssss/")
    assert response.status_code == 404


def test_status_302_redirect_login():
    response = flask_app.test_client().get("/postal_codes/")
    assert response.status_code == 302


def test_db_migrated():
    conf_json_reader = ConfJsonReader("/myApp/App/config_files/db_credentials_config.json")
    db_connector = DBConnector(conf_json_reader, DBConnectionManager)
    connection = db_connector.connect()
    cursor = connection.get_cursor()
    cursor.execute("select * from pay_stats;")
    cursor.execute("select * from postal_code;")
    cursor.execute("select * from app_user;")
    cursor.execute("select * from postal_code_polygon;")
    cursor.execute("select * from collected_polygon;")
    connection.close_connection()


def test_overlapping_polygon():
    conf_json_reader = ConfJsonReader("/myApp/App/config_files/db_credentials_config.json")
    db_connector = DBConnector(conf_json_reader, DBConnectionManager)
    connection = db_connector.connect()
    cursor = connection.get_cursor()
    cursor.execute(f"""
    update postal_code set the_geom = (select the_geom from postal_code where id='6061') where id = '6218';
    """)
    connection.close_connection()