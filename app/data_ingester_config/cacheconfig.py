""" Cache configuration for accountability_data_ingester"""
import os

REDIS_CONFIG = {
    "host": os.environ.get('REDIS_HOST', "localhost"),
    "port": os.environ.get('REDIS_PORT', 6379),
    "decode_responses": False,
    "password": os.environ.get('REDIS_PASSWORD', "redispass")
}