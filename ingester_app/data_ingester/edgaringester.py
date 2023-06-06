import json
from typing import List, Any

from ingester_app.data_ingester.constants.edgarconstants import HEADERS, SESSION_URL, COMPANY_TICKER_URL
from ingester_app.data_ingester.dataingester import DataIngester
from ingester_app.data_ingester_db.models.cik_ticker_mapping import CikTickerMapping
from ingester_app.data_ingester_logger.dataingesterlogger import DataIngesterLogger


class EDGARIngester(DataIngester):
    """
    Ingests data from the SEC EDGAR API.
    """

    def __init__(self):
        super().__init__()
        self.LOGGER = DataIngesterLogger("edgaringester")

    def ingest_transaction_by_ticker(self, ticker: str = None) -> json:
        """
        Pull
        :return:
        """

        try:
            self.LOGGER.info(f"Received a request to ingest data for ticker: {ticker}")
            return self._get_transaction_data_by_ticker(ticker)

        except Exception as e:
            self.LOGGER.error(f"Could not ingest data for ticker: {ticker}. Error: {e}")
            raise e

    def ingest_cik_ticker_mappings(self) -> List[CikTickerMapping]:
        """
        Pull down the latest company_ticker_mapping
        :return: The list of CikTickerMapping objects.
        """

        self.LOGGER.info("Pulling the latest cik_ticker_mapping data from EDGAR.")

        try:
            mappings = []
            company_tickers_response = self.data_fetcher.fetch(COMPANY_TICKER_URL, HEADERS)
            for idx, company_data in company_tickers_response.items():
                mappings.append(CikTickerMapping(cik_str=company_data["cik_str"],
                                                 ticker=company_data["ticker"],
                                                 title=company_data["title"]))
            return mappings

        except Exception as e:
            self.LOGGER.error(f"Could not get the latest cik_ticker_mapping data. Error: {e}")
            return []

    def ingest_companyfacts_data(self) -> List[Any]:
        """
        Pull down the latest company facts data.
        :return: The list of CompanyFacts objects.
        """

        self.LOGGER.info("Pulling the latest company_facts data from EDGAR.")
        return []

    def _get_transaction_data_by_ticker(self, ticker: str) -> json:
        """
        Get the EDGAR transaction data from the api by the ticker.
        :param ticker: company stock ticker. eg: "AAPL"
        :return: the json of the response from the api.
        """

        raise NotImplementedError

        # TODO this needs to be fixed to work with the new
        # paradigm for storing data.

        # try:
        #     self.LOGGER.info(f"Getting session transaction data by ticker: {ticker}")
              ## WE SHOULD QUERY THE DB FOR THIS NOW
        #     company_mapping = self._get_ticker_cik_mapping(ticker)
        #     cik = str(company_mapping["cik_str"]).rjust(CIK_LENGTH, '0')
        #     return self._retrieve_transaction_data(cik)
        #
        # except Exception as e:
        #     self.LOGGER.error(f"Could not get transaction data by ticker: {ticker}. Error: {e}")
        #     return make_response({"oopsie x3": "There was a wittle 404 x3B"}, 404)

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
