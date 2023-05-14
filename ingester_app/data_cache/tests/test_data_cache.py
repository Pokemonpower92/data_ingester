import pickle
from unittest import TestCase, mock

from ingester_app.data_cache.datacache import DataCache

data = {}


def mock_set(key, val):
    data[key] = val


def mock_get(key):
    return data.get(key, {})


class TestDataCache(TestCase):

    def setUp(self) -> None:
        data["VALID"] = pickle.dumps({"valid": "valid"})

    @mock.patch("redis.Redis.get")
    def test_invalid_get(self, mock_redis_get):
        mock_redis_get.side_effect = mock_get
        data_cache = DataCache()

        cache_miss = data_cache.get("INVALID")
        assert cache_miss == {}

    @mock.patch("redis.Redis.get")
    def test_valid_get(self, mock_redis_get):
        mock_redis_get.side_effect = mock_get
        data_cache = DataCache()

        cache_hit = data_cache.get("VALID")
        assert cache_hit == pickle.loads(data.get("VALID"))
