from ingester_app import db
from ingester_app.data_ingester.edgaringester import EDGARIngester
from ingester_app.data_ingester_async.celery import app


@app.task
def ingest_cik_ticker_mapping():
    EDGARIngester().ingest_cik_ticker_mappings()


@app.task
def ingest_recent_filings():
    EDGARIngester().ingest_recent_filings()
