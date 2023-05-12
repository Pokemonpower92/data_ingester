import os


class DataIngesterConfig:
    _mapping = {}

    def get_config(self, config):
        DEBUG = os.environ.get("DEBUG", "1")

        self._mapping = {
            "DEBUG": DEBUG
        }

        return self._mapping[config]


