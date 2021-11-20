import psycopg2
import logging

log = logging.getLogger(__name__)


class DBConnectionManager:
    """
    Responsible for establishing and closing a database connection.

    connect_db - returns a DB connection

    get_cursor - returns a DB cursor from the connection in order to execute SQL commands

    close_connection - closes the DB connection and the cursor
    """

    def __init__(self, host, user, password, db_name, port):

        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.port = port

    def connect_db(self, db_system=psycopg2):

        log.info(f"connecting to.... {db_system}")

        try:
            db_connection = db_system.connect(
                host=self.host,
                database=self.db_name,
                user=self.user,
                password=self.password,
                port=self.port,
            )
            db_connection.autocommit = True
            return db_connection

        except Exception as e:
            raise ConnectionError(f"ERROR connecting to {db_system}, {e}")

    def get_cursor(self):

        db_connection = self.connect_db()
        cursor = db_connection.cursor()

        return cursor

    def close_connection(self):
        cursor = self.get_cursor()
        db_connection = self.connect_db()
        cursor.close()
        db_connection.close()
