from ingester_app.data_ingester_async.celery import app


@app.task
def ingest_cik_ticker_mapping():
    return "ingesting_cik_ticker_mapping"


@app.task
def ingest_companyfacts_file():
    return "ingesting_companyfacts_file"
