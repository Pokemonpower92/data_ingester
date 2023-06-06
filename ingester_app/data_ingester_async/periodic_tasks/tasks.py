from ingester_app import db
from ingester_app.data_ingester.edgaringester import EDGARIngester
from ingester_app.data_ingester_async.celery import app


@app.task
def ingest_cik_ticker_mapping():
    db.session.add_all(EDGARIngester().ingest_cik_ticker_mappings())
    db.session.commit()


@app.task
def ingest_companyfacts_file():
    return "ingesting_companyfacts_file"
