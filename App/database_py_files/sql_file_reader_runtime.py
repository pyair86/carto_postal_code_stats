import logging

log = logging.getLogger(__name__)


class SqlFileRuntimeReader:
    def __init__(self):
        pass

    @staticmethod
    def read_file(sql_file):
        log.info(f"reading SQL file.... {sql_file}")
        with open(sql_file) as file:
            sql_file_content = file.read()

        return sql_file_content

    def read_select_single_geom_queries(
        self,
        path_get_geojson_single_polygon="/myApp/App/data_access_layer/queries/get_geojson_single_polygon",
        path_get_aggregated_turnover_single_polygon="/myApp/App/data_access_layer/queries/get_aggregated_turnover_single_polygon",
    ):
        get_geojson_single_polygon = self.read_file(path_get_geojson_single_polygon)
        get_aggregated_turnover_single_polygon = self.read_file(
            path_get_aggregated_turnover_single_polygon
        )
        return get_geojson_single_polygon, get_aggregated_turnover_single_polygon

    def read_select_collected_geom_queries(
        self,
        path_get_geojson_collected_polygon="/myApp/App/data_access_layer/queries/get_geojson_collected_polygon",
        path_get_aggregated_turnover_all_polygons="/myApp/App/data_access_layer/queries/get_aggregated_turnover_all_polygons",
    ):
        get_geojson_collected_polygon = self.read_file(
            path_get_geojson_collected_polygon
        )
        get_aggregated_turnover_all_polygons = self.read_file(
            path_get_aggregated_turnover_all_polygons
        )
        return get_geojson_collected_polygon, get_aggregated_turnover_all_polygons

    def read_register_user(
        self, path_register_user="/myApp/App/data_access_layer/insert/register_user"
    ):
        read_register_user = self.read_file(path_register_user)
        return read_register_user

    def read_get_user_password(
        self, path_get_user_password="App/data_access_layer/queries/get_user_password"
    ):
        get_user_password = self.read_file(path_get_user_password)
        return get_user_password
