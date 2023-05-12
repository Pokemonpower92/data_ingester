import pickle
from datetime import timedelta
from typing import Any, Dict

import redis

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
