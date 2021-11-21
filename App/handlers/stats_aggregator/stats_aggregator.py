#!/usr/bin/python
# -*- coding: utf-8 -*-


class StatsPolygonAggregator:

    """
    Responsible for aggregating the statistical and integration with the
    geojson.

    Inner loop in aggregate_data should not be that bad
    because usually there aren't so many columns in a table.
    """

    def __init__(
        self,
        cursor,
        geo_json_query,
        agg_postal_code_data_query,
        postal_code=None,
        aggregator_column='p_age',
        ):

        self.cursor = cursor
        self.postal_code = postal_code
        self.geo_json_query = geo_json_query
        self.agg_postal_code_data_query = agg_postal_code_data_query
        self.aggregator_column = aggregator_column

    @staticmethod
    def aggregate_data(data_rows, column_names):
        aggregated_result = []

        for data_row in data_rows:

            statistics = {}

            for (index, column_name) in enumerate(column_names):
                statistics[column_name] = data_row[index]

            aggregated_result.append(statistics)

        return aggregated_result

    def get_geojson_geom_coordinates(self):
        self.cursor.execute(self.geo_json_query, (self.postal_code, ))
        query_result = self.cursor.fetchone()
        if query_result:
            geojson = query_result[0]
            return geojson
        return False

    def get_postal_code_stats(self):
        self.cursor.execute(self.agg_postal_code_data_query,
                            (self.postal_code, ))
        postal_code_stats = self.cursor.fetchall()
        return postal_code_stats

    def get_geojson_aggregated_stats(self):
        collected_stats_json_agg_column = None
        geojson = self.get_geojson_geom_coordinates()
        postal_code_stats = self.get_postal_code_stats()
        if not postal_code_stats:
            return False
        db_postal_code_column_names = [desc[0] for desc in
                self.cursor.description]

        collected_stats_json = self.aggregate_data(postal_code_stats,
                db_postal_code_column_names)

        if self.aggregator_column:
            collected_stats_json_agg_column = \
                self.aggregate_stats_per_column(collected_stats_json)

        geo_json_properties = geojson['features'][0]['properties']
        if not self.aggregator_column:
            geo_json_properties['population_stats'] = \
                collected_stats_json
        else:
            geo_json_properties['population_stats'] = \
                collected_stats_json_agg_column

        # avoid duplications of coordinates in json - not necessary in properties

        del geo_json_properties['the_geom']

        # id should not be so relevant for frontend

        del geo_json_properties['id']

        return geojson

    def set_column_aggregator(self, population_stats):
        result = []

        for stat in population_stats:
            new_agg_column = stat[self.aggregator_column]
            del stat[self.aggregator_column]
            result.append({new_agg_column: stat})

        return result

    def aggregate_stats_per_column(self, population_stats):
        aggregated_stats = {}
        stats_with_column_aggregator = \
            self.set_column_aggregator(population_stats)
        for (index, stat) in enumerate(stats_with_column_aggregator):
            for (agg_column_value, ungrouped_stats) in stat.items():
                if index < len(stats_with_column_aggregator) - 1:
                    if agg_column_value \
                        in stats_with_column_aggregator[index + 1]:
                        aggregated_stats[agg_column_value] = \
                            [ungrouped_stats,
                             stats_with_column_aggregator[index
                             + 1][agg_column_value]]

        result = {self.aggregator_column: aggregated_stats}
        return result
