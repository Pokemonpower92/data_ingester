from flask import Flask
app = Flask(__name__)
from app import views, data_ingester, data_fetcher, data_cache, data_ingester_config
