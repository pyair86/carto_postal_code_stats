from App.main import ConfJsonReader
from App.database_py_files.db_connection_manager import DBConnectionManager
from App.database_py_files.db_connector import DBConnector

"""
Should test an empty DB in a real project
"""

def test_db_migrated():
    conf_json_reader = ConfJsonReader("/myApp/App/config_files/db_credentials_config.json")
    db_connector = DBConnector(conf_json_reader, DBConnectionManager)
    connection = db_connector.connect()
    cursor = connection.get_cursor()
    cursor.execute("select * from information_schema.tables where table_name=%s", ('pay_stats',))
    assert cursor.fetchone() is not None
    cursor.execute("select * from information_schema.tables where table_name=%s", ('postal_code',))
    assert cursor.fetchone() is not None
    cursor.execute("select * from information_schema.tables where table_name=%s", ('app_user',))
    assert cursor.fetchone() is not None
    cursor.execute("select * from information_schema.tables where table_name=%s", ('postal_code_polygon',))
    assert cursor.fetchone() is not None
    cursor.execute("select * from information_schema.tables where table_name=%s", ('collected_polygon',))
    assert cursor.fetchone() is not None
    cursor.execute("select * from information_schema.tables where table_name=%s", ('paella',))
    assert cursor.fetchone() is None
    connection.close_connection()


def test_no_overlapping_polygons():
    conf_json_reader = ConfJsonReader("/myApp/App/config_files/db_credentials_config.json")
    db_connector = DBConnector(conf_json_reader, DBConnectionManager)
    connection = db_connector.connect()
    cursor = connection.get_cursor()
    cursor.execute(f"""
    SELECT
        a.id
    FROM
        postal_code a INNER JOIN postal_code b
     ON
        (a.the_geom && b.the_geom AND ST_Relate(a.the_geom, b.the_geom, '2********'))
     WHERE
        a.ctid != b.ctid LIMIT 1;""")
    assert cursor.fetchone() is None
    connection.close_connection()
