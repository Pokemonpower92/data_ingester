import json

from flask import make_response

from app.data_ingester.constants.edgarconstants import HEADERS, CIK_LENGTH, \
     SESSION_URL, COMPANY_TICKER_URL
from app.data_ingester.dataingester import DataIngester


class EDGARInjester(DataIngester):
    """
    Ingests data from the SEC EDGAR API.
    """

    def ingest(self, ticker: str = None) -> json:
        """
        Pull down data from EDGAR and populate the
        company_ticker_mapping, then fetch the data
        from EDGAR.
        :return:
        """

        try:
            return self._get_transaction_data_by_ticker(ticker)

        except Exception as e:
            print("Couldn't ingest Edgar Data.")
            print(e)

    def _get_ticker_cik_mapping(self, ticker: str) -> str:
        """
        Pull down the latest company_ticker_mapping
        :type ticker: the ticker to map to.
        :return: the CIK of the company.
        """

        # Get the data from cache, if it exists.
        # Cache it if it doesn't.
        cache_value = self.data_cache.get(ticker)
        if not cache_value:
            company_tickers_response = self.data_fetcher.fetch(COMPANY_TICKER_URL, HEADERS)

            for id, company_data in company_tickers_response.items():
                if ticker == company_data["ticker"]:
                    cache_value = self.data_cache.cache(ticker, company_data)

        return cache_value

    def _get_transaction_data_by_ticker(self, ticker: str) -> json:
        """
        Get the EDGAR transaction data from the api by the ticker.
        :param ticker: company stock ticker. eg: "AAPL"
        :return: the json of the response from the api.
        """

        try:
            company_mapping = self._get_ticker_cik_mapping(ticker)
            cik = str(company_mapping["cik_str"]).rjust(CIK_LENGTH, '0')
            return self._retrieve_transaction_data(cik)

        except Exception as e:
            return make_response({"oopsie x3": "There was a wittle 404 x3B"}, 404)

    def _retrieve_transaction_data(self, cik: str) -> json:
        """
        Either fetch the session endpoint data from cache or the
        endpoint.
        :param cik: cik of the company.
        :return: the transaction data response from EDGAR's sessions endpoint.
        """

        print("getting session data.")
        session_data = self.data_cache.get_session_json(cik)
        if not session_data:
            print("cache miss")
            session_data = self.data_cache.cache_session_json(cik, self.data_fetcher.fetch(SESSION_URL.format(cik), HEADERS))

        return session_data
