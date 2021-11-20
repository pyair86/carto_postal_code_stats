import json
import logging

log = logging.getLogger(__name__)


class ConfJsonReader:
    """
    Responsible for reading configurations from config JSON files, so changes of configs
    such as password, username... won't cause modifications of PY code.
    """

    def __init__(self, json_conf_path):
        self.json_conf_path = json_conf_path

    def load_json(self):

        log.info(f"loading conf file: {self.json_conf_path}")
        try:
            with open(self.json_conf_path, encoding="utf8") as json_file:
                conf_json = json.load(json_file)
                return conf_json

        except Exception as e:
            log.error(f"ERROR reading the conf file: {self.json_conf_path}, {e}")

    def get_config(self, config):
        try:

            loaded_json = self.load_json()

            log.info(f"getting {config} conf")

            config_value = loaded_json[config]
            return config_value
        except Exception as e:
            log.error(f"ERROR getting the {config} conf: {e}")
