from app import app

from app.data_ingester.edgaringester import EDGARIngester


@app.route("/")
def index():
    return "Hello world"


@app.route("/edgar/<ticker>")
def edgar(ticker: str) -> str:
    return EDGARIngester().ingest(ticker)
