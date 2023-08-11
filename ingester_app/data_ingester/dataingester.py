import json

from ingester_app.data_cache.datacache import DataCache
from ingester_app.data_fetcher.datafetcher import DataFetcher


class DataIngester:
    """
    A data ingester pulls data from the api for a particular
    data source (eg: the SEC EDGAR data set) and stores it
    away in the database.
    """

    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.data_cache = DataCache()
