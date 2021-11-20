import logging

log = logging.getLogger(__name__)


class SqlFileMigrationReader:
    """
    Responsible for reading content in text files with SQL commands.
    Point was to give flexibility when changing commands without modifying the PY code.

    read_migrate_commands - reads SQL commands for when the DB is initiated:
    Order of executions is important, no_overlapping_function must be implemented before
    geometries are entering to the table.
    read_set_fkey must be executed after the tables are populated
    because of the parallel insert into tables.

    read_geom_edit_commands - define a single type geom in the table so we can apply
    geom constraints (e.g. polygons only) in the geom column.
    """

    def __init__(self):
        pass

    @staticmethod
    def read_file(sql_file):
        log.info(f"reading SQL file.... {sql_file}")
        with open(sql_file) as file:
            sql_file_content = file.read()

        return sql_file_content

    def read_migrate_commands(
        self,
        path_create_tables="App/data_access_layer/create/create_tables",
        path_set_constraints="App/data_access_layer/alter/set_constraints",
        path_check_no_overlapping_polygons="App/data_access_layer/functions/check_no_overlapping_polygons",
    ):
        create_tables = self.read_file(path_create_tables)
        set_constraints = self.read_file(path_set_constraints)
        check_no_overlapping_polygons = self.read_file(
            path_check_no_overlapping_polygons
        )

        return create_tables, check_no_overlapping_polygons, set_constraints

    def read_geom_edit_commands(
        self,
        path_create_dumped_polygon_table="App/data_access_layer/create/create_dumped_polygon_table",
        path_make_polygon_multipolygon="App/data_access_layer/alter/make_polygon_multipolygon",
        path_dumped_collected_polygon_table="App/data_access_layer/create/create_dumped_collected_polygon_table",
    ):

        create_dumped_polygon_table = self.read_file(path_create_dumped_polygon_table)
        make_polygon_multipolygon = self.read_file(path_make_polygon_multipolygon)
        dumped_collected_polygon_table = self.read_file(
            path_dumped_collected_polygon_table
        )

        return (
            create_dumped_polygon_table,
            make_polygon_multipolygon,
            dumped_collected_polygon_table,
        )

    def read_set_fkey(
        self,
        path_add_fkey_pay_stats="/myApp/App/data_access_layer/alter/add_fkey_pay_stats",
    ):
        add_fkey_pay_stats = self.read_file(path_add_fkey_pay_stats)
        return add_fkey_pay_stats
