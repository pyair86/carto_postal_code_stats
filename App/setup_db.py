import psycopg2
from database_py_files.sql_executer import SqlExecuter
from logger.logger import Logger
import logging
from database_py_files.db_connector import DBConnector
from conf_file_reader.conf_json_reader import ConfJsonReader
from database_py_files.db_connection_manager import DBConnectionManager
from database_py_files.sql_file_reader_migration import SqlFileMigrationReader

log = logging.getLogger(__name__)

conf_json_reader = ConfJsonReader("/myApp/App/config_files/db_credentials_config.json")
db_connector = DBConnector(conf_json_reader, DBConnectionManager)

conf_json_reader = ConfJsonReader("/myApp/App/config_files/csv_config.json")
csv_path_sql_command_path = conf_json_reader.get_config("paths_csv_sql_command")


def setup_data():
    db_connection = None
    try:
        Logger()
        db_connection = db_connector.connect()
        sql_file_reader = SqlFileMigrationReader()
        sql_executer = SqlExecuter(db_connection.get_cursor())

        migrate_commands = sql_file_reader.read_migrate_commands()
        geom_edit_commands = sql_file_reader.read_geom_edit_commands()
        set_fkey = sql_file_reader.read_set_fkey()

        sql_executer.execute_iteration(migrate_commands)
        sql_executer.execute_parallel_copy_csv(csv_path_sql_command_path, db_connection)
        sql_executer.execute(set_fkey)
        sql_executer.execute_iteration(geom_edit_commands)

        log.info("migrated successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        log.error(error)

    finally:
        db_connection.close_connection()


if __name__ == "__main__":
    setup_data()
