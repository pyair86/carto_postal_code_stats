class DBConnector:
    """
    Responsible for passing DB configs values from config JSON to the DBConnectionManager,
    in order to establish a DB connection
    """

    def __init__(self, conf_json_reader, db_connection_manager):
        self.conf_json_reader = conf_json_reader
        self.db_connection_manager = db_connection_manager

    def connect(
        self,
        db_host="db_host",
        db_password="db_password",
        db_user="db_user",
        db_name="db_name",
        db_port="db_port",
    ):
        db_host = self.conf_json_reader.get_config(db_host)
        db_password = self.conf_json_reader.get_config(db_password)
        db_user = self.conf_json_reader.get_config(db_user)
        db_name = self.conf_json_reader.get_config(db_name)
        db_port = self.conf_json_reader.get_config(db_port)
        return self.db_connection_manager(
            db_host, db_user, db_password, db_name, db_port
        )
