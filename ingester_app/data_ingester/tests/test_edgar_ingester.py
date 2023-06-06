from unittest import TestCase, mock
import unittest

import pytest

from ingester_app.data_ingester.edgaringester import EDGARIngester


def mock_ticker_mapping(success: bool) -> dict:
    status_code = 200 if success else 404
    message = ":)" if success else ":("

    return {
        "status_code": status_code,
        "body": {
            "message": message,
            "cik_str": "1"
        }
    }


def mock_transaction_data(success: bool) -> dict:

    status_code = 200 if success else 404
    message = ":)" if success else ":("

    return {
        "status_code": status_code,
        "body": {
            "message": message
        }
    }


def get_mock_response(success: bool):

    class MockResponse:
        def __init__(self):
            self.status_code = None
            self.body = None

        def fail(self):
            self.status_code = 404
            self.body = {"message": ":("}
            return self

        def success(self):
            self.status_code = 200
            self.body = {"message": ":)"}
            return self

    if success:
        return MockResponse().success()
    else:
        return MockResponse().fail()

class TestEdgarIngester(TestCase):

    module_string = "ingester_app.data_ingester.edgaringester"
    class_string = module_string + ".EDGARIngester"

    @mock.patch(class_string+"._get_transaction_data_by_ticker")
    @unittest.skip("Not implemented")
    def test_ingest(self, mock_get_transaction):
        ingester = EDGARIngester()
        mock_get_transaction.side_effect = Exception("mock")
        self.assertRaises(Exception, ingester.ingest, "mock")

    @mock.patch(class_string + "._get_ticker_cik_mapping")
    @mock.patch(class_string + "._retrieve_transaction_data")
    @mock.patch(module_string + ".make_response")
    @unittest.skip("Not implemented")
    def test_get_transaction_data_by_id(self, mock_response, mock_transaction, mock_ticker):
        ingester = EDGARIngester()

        mock_ticker.return_value = mock_ticker_mapping(True)
        mock_transaction.side_effect = Exception()
        mock_response.return_value = get_mock_response(False)
        response = ingester._get_transaction_data_by_ticker("AAPL")

        assert response.status_code == 404

        mock_ticker.side_effect = Exception()
        mock_transaction.return_value = mock_transaction_data(False)
        mock_response.return_value = get_mock_response(False)
        response = ingester._get_transaction_data_by_ticker("AAPL")

        assert response.status_code == 404

        mock_ticker.side_effect = mock_ticker_mapping(True)
        mock_transaction.return_value = mock_transaction_data(True)
        mock_response.return_value = get_mock_response(True)
        response = ingester._get_transaction_data_by_ticker("AAPL")

        assert response.status_code == 200
