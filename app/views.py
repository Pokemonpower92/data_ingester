from app import app

from app.data_ingester.edgaringester import EDGARInjester


@app.route("/")
def index():
    print("Index prints.")
    return "Hello world"


@app.route("/edgar/<ticker>")
def edgar(ticker: str) -> str:
    return EDGARInjester().ingest(ticker)
