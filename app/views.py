from app import app

from app.data_ingester.edgaringester import EDGARIngester
from app.data_ingester_config.limitconfig import NINE_A_SECOND
from app.data_ingester_limiter.dataingesterlimiter import data_ingester_limiter


@app.route("/")
def index():
    return "Hello world"


@app.route("/edgar/<ticker>")
@data_ingester_limiter.limit(NINE_A_SECOND)
def edgar(ticker: str) -> str:
    return EDGARIngester().ingest(ticker)
