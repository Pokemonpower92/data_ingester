import json
import pickle
from datetime import timedelta
from typing import Any, Dict

import redis
from redis.commands.json.path import Path

from app.data_ingester_config.cacheconfig import REDIS_CONFIG


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
        self.cache_instance.setex(key, timedelta(minutes=1), p_dict)
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

        self.cache_instance.json().set(f"{cik}:response", "$", response)
        self.cache_instance.setex(f"{cik}:timer", timedelta(seconds=20), "NONE")

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
        if not self.cache_instance.get(f"{cik}:timer"):
            self.cache_instance.json().delete(f"{cik}:response")
            return {}
        else:
            return self.cache_instance.json().get(f"{cik}:response")
