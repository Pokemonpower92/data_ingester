from ingester_app import db
from ingester_app.blueprints.edgar.models.cik_ticker_mapping import CikTickerMapping
from ingester_app.data_ingester_async.celery import app


@app.task
def ingest_cik_ticker_mapping():
    test_mapping = CikTickerMapping("1", "0001", "Test")
    db.session.add(test_mapping)
    db.session.commit()


@app.task
def ingest_companyfacts_file():
    return "ingesting_companyfacts_file"
