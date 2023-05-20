""" Cache configuration for accountability_data_ingester"""
import os
from datetime import timedelta

from ingester_app.data_ingester_config.dataingesterconfig import DataIngesterConfig

REDIS_HOST = os.environ.get('REDIS_HOST', "localhost")
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
REDIS_USER = os.environ.get('REDIS_USER', "guest")
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', "redispass")

REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"

REDIS_CONFIG = {
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "decode_responses": False,
    "password": REDIS_PASSWORD
}

TICKER_MAPPING_KEY = "ticker_mapping"
SESSION_EX_KEY = "{}:ex"
SESSION_DATA_KEY = "{}:data"

# Debug-specific configurations.
if int(DataIngesterConfig().get_config("DEBUG")):
    TICKER_MAPPING_EX = SESSION_DATA_EX = timedelta(seconds=30)
else:
    TICKER_MAPPING_EX = SESSION_DATA_EX = timedelta(days=1)


