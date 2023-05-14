import json

from flask import make_response

from ingester_app.data_ingester.constants.edgarconstants import HEADERS, CIK_LENGTH, \
     SESSION_URL, COMPANY_TICKER_URL
from ingester_app.data_ingester.dataingester import DataIngester
from ingester_app.data_ingester_logger.dataingesterlogger import DataIngesterLogger


class EDGARIngester(DataIngester):
    """
    Ingests data from the SEC EDGAR API.
    """

    def __init__(self):
        super().__init__()
        self.LOGGER = DataIngesterLogger("edgaringester")

    def ingest(self, ticker: str = None) -> json:
        """
        Pull down data from EDGAR and populate the
        company_ticker_mapping, then fetch the data
        from EDGAR.
        :return:
        """

        try:
            self.LOGGER.info(f"Received a request to ingest data for ticker: {ticker}")
            return self._get_transaction_data_by_ticker(ticker)

        except Exception as e:
            self.LOGGER.error(f"Could not ingest data for ticker: {ticker}. Error: {e}")
            raise e

    def _get_ticker_cik_mapping(self, ticker: str) -> str:
        """
        Pull down the latest company_ticker_mapping
        :type ticker: the ticker to map to.
        :return: the CIK of the company.
        """

        # Get the data from cache, if it exists.
        # Cache it if it doesn't.
        self.LOGGER.info("Fetching ticker to cik mapping from cache.")
        cache_value = self.data_cache.get(ticker)
        if not cache_value:
            self.LOGGER.info("Ticker to cik mapping was uncached. Caching.")
            company_tickers_response = self.data_fetcher.fetch(COMPANY_TICKER_URL, HEADERS)

            for idx, company_data in company_tickers_response.items():
                if ticker == company_data["ticker"]:
                    cache_value = self.data_cache.cache(ticker, company_data)

        self.LOGGER.info("Ticker to cik mapping fetched.")
        return cache_value

    def _get_transaction_data_by_ticker(self, ticker: str) -> json:
        """
        Get the EDGAR transaction data from the api by the ticker.
        :param ticker: company stock ticker. eg: "AAPL"
        :return: the json of the response from the api.
        """

        try:
            self.LOGGER.info(f"Getting session transaction data by ticker: {ticker}")
            company_mapping = self._get_ticker_cik_mapping(ticker)
            cik = str(company_mapping["cik_str"]).rjust(CIK_LENGTH, '0')
            return self._retrieve_transaction_data(cik)

        except Exception as e:
            self.LOGGER.error(f"Could not get transaction data by ticker: {ticker}. Error: {e}")
            return make_response({"oopsie x3": "There was a wittle 404 x3B"}, 404)

    def _retrieve_transaction_data(self, cik: str) -> json:
        """
        Either fetch the session endpoint data from cache or the
        endpoint.
        :param cik: cik of the company.
        :return: the transaction data response from EDGAR's sessions endpoint.
        """

        self.LOGGER.info(f"Fetching session data for cik: {cik} from cache.")
        session_data = self.data_cache.get_session_json(cik)
        if not session_data:
            self.LOGGER.info(f"Session data for cik: {cik} uncached. Caching")
            session_data = self.data_cache.cache_session_json(cik, self.data_fetcher.fetch(SESSION_URL.format(cik), HEADERS))

        self.LOGGER.info(f"Successfully retrieved session data for cik: {cik}.")
        return session_data
