from unittest import TestCase, mock
from requests import Response

from ingester_app.data_fetcher.datafetcher import DataFetcher

mock_request = {
    "endpoint": "blah",
    "headers": {"fake": "fake"}
}


def mock_get(endpoint, headers):
    mock_response = Response()
    mock_response.url = endpoint
    mock_response.headers = headers
    return mock_response


class TestDataFetcher(TestCase):

    @mock.patch("ingester_app.data_fetcher.datafetcher.requests.get")
    @mock.patch("ingester_app.data_fetcher.datafetcher.requests.Response.json")
    def test_fetch(self, mocked_json, mocked_get):
        data_fetcher = DataFetcher()
        mocked_get.return_value = mock_get("blah", {"fake": "fake"})
        mocked_json.return_value = mock_request
        result = data_fetcher.fetch(mock_request["endpoint"], mock_request["headers"])

        assert result == mock_request
