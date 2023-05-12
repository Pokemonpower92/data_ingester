""" Cache configuration for accountability_data_ingester"""
import os
from datetime import timedelta

from app.data_ingester_config.dataingesterconfig import DataIngesterConfig

REDIS_CONFIG = {
    "host": os.environ.get('REDIS_HOST', "localhost"),
    "port": os.environ.get('REDIS_PORT', 6379),
    "decode_responses": False,
    "password": os.environ.get('REDIS_PASSWORD', "redispass")
}

TICKER_MAPPING_KEY = "ticker_mapping"
SESSION_EX_KEY = "{}:ex"
SESSION_DATA_KEY = "{}:data"

# Debug-specific configurations.
if int(DataIngesterConfig().get_config("DEBUG")):
    TICKER_MAPPING_EX = SESSION_DATA_EX = timedelta(seconds=30)
else:
    TICKER_MAPPING_EX = SESSION_DATA_EX = timedelta(days=1)


