import io
import json

import requests

from ingester_app.data_ingester_logger.dataingesterlogger import DataIngesterLogger


class DataFetcher:

    def __init__(self):
        self.LOGGER = DataIngesterLogger("datafetcher")

    def fetch_json(self, endpoint: str, headers: json = None) -> json:
        """
        fetch json data from the endpoint.
        :param endpoint: the endpoint to query.
        :param headers: the headers to use, if any.
        :return: the json that is returned from the endpoint.
        """

        try:
            self.LOGGER.info(f"Received request to fetch json data from: {endpoint} with headers: {headers}")
            response = requests.get(endpoint, headers=headers)
            return response.json()

        except Exception as e:
            self.LOGGER.error(f"Failed to fetch json data from: {endpoint} with headers: {headers}. Error: {e}")

    def fetch_file(self, endpoint: str, headers: json = None) -> io.BytesIO:
        """
        Fetch a file from the given endpoint with the given headers.
        :param endpoint: the endpoint to query.
        :param headers: the headers to use, if any.
        :return: a byte-stream from the endpoint.
        """

        try:
            self.LOGGER.info(f"Received request to fetch file data from: {endpoint} with headers: {headers}")
            response = requests.get(endpoint, headers=headers, stream=True)
            return io.BytesIO(response.content)

        except Exception as e:
            self.LOGGER.error(f"Failed to fetch file data from: {endpoint} with headers: {headers}. Error: {e}")
            