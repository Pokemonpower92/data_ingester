import json

from flask import abort, make_response, jsonify

from app.data_ingester.constants.edgarconstants import COMPANY_TICKER_KEY, COMPANY_TICKERS, HEADERS, CIK_LENGTH, \
    SESSION, SESSION_URL, COMPANY_TICKER_URL
from app.data_ingester.dataingester import DataIngester
from app.data_ingester_error.dataingestererror import DataIngesterError


class EDGARInjester(DataIngester):
    """
    Ingests data from the SEC EDGAR API.
    """

    def ingest(self, ticker: str) -> json:
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
            response = self.data_fetcher.fetch(SESSION_URL.format(cik), HEADERS)

            ##TODO these should be cached for each company:
            # by accessing response["filings"]["recent"]
            #       recent.accessionNumber
            #       recent.filingDate
            #       recent.reportDate
            #       recent.acceptanceDateTime
            #       recent.act
            #       recent.form
            #       recent.fileNumber
            #       recent.filmNumber
            #       recent.items
            #       recent.size
            #       recent.isXBRL
            #       recent.isInlineXBRL
            #       recent.primaryDocument
            #       recent.primaryDocDescription
            # It should be keyed by CIK+recent

            ##TODO Probably want to cache this. these are historical records.
            # response["filings"]["files"]

            return response

        except Exception as e:
            return make_response({"oopsie x3": "There was a wittle 404 x3B"}, 404)
