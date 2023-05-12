import json

import requests


class DataFetcher:

    def fetch(self, endpoint: str, headers: json = None) -> json:
        """
        fetch the data from the endpoint.
        :param endpoint: the endpoint to query.
        :param headers: the headers to use, if any.
        :return: the json that is returned from the endpoint.
        """

        response = requests.get(endpoint, headers=headers)
        return response.json()
