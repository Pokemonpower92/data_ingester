import json
import pickle
from typing import Any, Dict

import redis
from redis.commands.json.path import Path

from ingester_app.data_ingester_config.cacheconfig import REDIS_CONFIG, TICKER_MAPPING_EX, SESSION_DATA_EX, SESSION_DATA_KEY, \
    SESSION_EX_KEY


class DataCache:
    """
    DataCache is the cache proxy for data ingesters.
    It is currently back-ended by redis.
    """

    def __init__(self) -> None:
        self.cache_instance = redis.Redis(**REDIS_CONFIG)

    def cache(self, key: str, value: Dict[str, Any]) -> None:
        """
        Store the given data in redis.
        :param key: cache key
        :param value: cache value.
        :return:
        """

        p_dict = pickle.dumps(value)
        self.cache_instance.setex(key, TICKER_MAPPING_EX, p_dict)
        return pickle.loads(self.cache_instance.get(key))

    def get(self, key: str) -> Dict[str, Any]:
        """
        get the value from cache by key
        :param key: the cache key.
        :return: the value from cache if it exists.
        """

        entry = self.cache_instance.get(key)
        if entry:
            return pickle.loads(entry)
        else:
            return {}

    def cache_session_json(self, cik: str, response: json) -> json:
        """
        Store the session json in cache then return it.
        :param cik: the cik of the company to cache data for.
        :param response: the response to cache.
        :return: the cached response.
        """

        self.cache_instance.json().set(SESSION_DATA_KEY.format(cik), "$", response)
        self.cache_instance.setex(SESSION_EX_KEY.format(cik), SESSION_DATA_EX, "NONE")

        return response

    def get_session_json(self, cik: str) -> json:
        """
        Retrieve the response by cik, if it's within the cache window.
        Otherwise, delete the entry.
        :param cik: cik of the company whose data we're storing.
        :return: the data store that was fetched, if it's still cached.
        """

        # We only want to cache this for a single day, as the reports update daily.
        # We'll use a separate key-value pair to delete the response on schedule,
        # as redisJSON doesn't support setx.
        if not self.cache_instance.get(SESSION_EX_KEY.format(cik)):
            self.cache_instance.json().delete(SESSION_DATA_KEY.format(cik))
            return {}
        else:
            return self.cache_instance.json().get(SESSION_DATA_KEY.format(cik))
