import json

import requests

from app.data_ingester_logger.dataingesterlogger import DataIngesterLogger


class DataFetcher:

    def __init__(self):
        self.LOGGER = DataIngesterLogger("datafetcher")

    def fetch(self, endpoint: str, headers: json = None) -> json:
        """
        fetch the data from the endpoint.
        :param endpoint: the endpoint to query.
        :param headers: the headers to use, if any.
        :return: the json that is returned from the endpoint.
        """

        self.LOGGER.info(f"Received request to fetch data from: {endpoint} with headers: {headers}")
        response = requests.get(endpoint, headers=headers)
        return response.json()
