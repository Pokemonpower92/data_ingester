import json
from zipfile import ZipFile

from ingester_app import db
from ingester_app.data_ingester.constants.edgarconstants import HEADERS, COMPANY_TICKER_URL, SUBMISSIONS_ZIP_URL
from ingester_app.data_ingester.dataingester import DataIngester
from ingester_app.data_ingester_db.models.cik_ticker_mapping import CikTickerMapping
from ingester_app.data_ingester_logger.dataingesterlogger import DataIngesterLogger

import pandas as pd


class EDGARIngester(DataIngester):
    """
    Ingests data from the SEC EDGAR API.
    """

    def __init__(self):
        super().__init__()
        self.LOGGER = DataIngesterLogger("edgaringester")

    def ingest_cik_ticker_mappings(self) -> None:
        """
        Pull down the latest company_ticker_mapping
        :return: None
        """

        self.LOGGER.info("Pulling the latest cik_ticker_mapping data from EDGAR.")

        try:
            mappings = []
            company_tickers_response = self.data_fetcher.fetch_json(COMPANY_TICKER_URL, HEADERS)
            for idx, company_data in company_tickers_response.items():
                mappings.append(CikTickerMapping(cik_str=company_data["cik_str"],
                                                 ticker=company_data["ticker"],
                                                 title=company_data["title"]))

            db.session.add_all(mappings)
            db.session.commit()

        except Exception as e:
            self.LOGGER.error(f"Could not get the latest cik_ticker_mapping data. Error: {e}")

    def ingest_recent_filings(self) -> None:
        """
        Pull down the latest submissions zip file from EDGAR and store them in
        the recent_filing table.
        :return: None
        """

        try:
            self.LOGGER.info("Pulling the latest recent filings data from EDGAR.")
            submissions_zip = self.data_fetcher.fetch_file(SUBMISSIONS_ZIP_URL, HEADERS)
            recent_filings = pd.DataFrame()

            with ZipFile(submissions_zip, 'r') as zipObj:
                for submission_file in zipObj.namelist():
                    try:
                        json_data = json.loads(zipObj.read(submission_file).decode())

                        # Load the json data into a data frame so we can easily clean it
                        # for storage in the database.
                        new_filings = pd.DataFrame(json_data["filings"]["recent"])
                        new_filings['cik_str'] = json_data['cik']

                        recent_filings = pd.concat([recent_filings, new_filings], ignore_index=True)

                    except Exception as e:
                        self.LOGGER.error(f"Error Reading submission file: {e}")

            # Store the aggregate filings in the recent_filing table.
            recent_filings.to_sql(name='recent_filing', if_exists='replace', con=db.engine, index=False)

        except Exception as e:
            self.LOGGER.error(f"Could not get the latest recent filing data. Error: {e}")
