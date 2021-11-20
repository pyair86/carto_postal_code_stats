from .sql_file_reader_migration import SqlFileMigrationReader
import logging
import concurrent.futures

log = logging.getLogger(__name__)


class SqlExecuter:
    """
    prepare_data_for_multithreading - prepares lists from the input dictionary -
    for an easy zip iteration when multithreaded.

    execute_parallel_copy_csv - a new cursor is made
    for each CSV file so the DB will be available to execute the transaction on parallel.
    Usage there should be careful though and well measured. E.g. maybe the data size won't worth it,
    and then a single thread might be enough. It can be achieved with (max_workers=1) in ThreadPoolExecutor.

    copy_from_csv - COPY CSV was chosen due to its efficiency over other insert methods.
    """

    def __init__(self, cursor):
        self.cursor = cursor

    def execute_iteration(self, sql_commands):
        for sql_command in sql_commands:
            log.info(f"executing {sql_command}")
            self.cursor.execute(sql_command)

    def execute(self, sql_command):
        log.info(f"executing {sql_command}")
        self.cursor.execute(sql_command)

    @staticmethod
    def prepare_data_for_multithreading(csv_paths_copy_paths):
        paths = []
        copy_commands = []
        for path, copy_command in csv_paths_copy_paths.items():
            paths.append(path)
            copy_commands.append(copy_command)
        return paths, copy_commands

    @staticmethod
    def copy_from_csv(
        path, cursor, copy_command, sql_file_reader=SqlFileMigrationReader
    ):
        with open(path) as file:
            log.info(f"copying.... {copy_command}")
            sql_file_reader = sql_file_reader()
            cursor.copy_expert(sql=sql_file_reader.read_file(copy_command), file=file)
            cursor.close()

    def execute_parallel_copy_csv(self, csv_paths_copy_paths, db_connection):
        paths, copy_commands = self.prepare_data_for_multithreading(
            csv_paths_copy_paths
        )
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for path, copy_command in zip(paths, copy_commands):
                cursor = db_connection.get_cursor()
                futures.append(
                    executor.submit(
                        self.copy_from_csv,
                        path=path,
                        copy_command=copy_command,
                        cursor=cursor,
                    )
                )
