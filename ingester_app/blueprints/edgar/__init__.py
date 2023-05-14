from flask import Blueprint, render_template, current_app

from ingester_app.data_ingester.edgaringester import EDGARIngester
from ingester_app.data_ingester_config.limitconfig import NINE_A_SECOND
from ingester_app.data_ingester_limiter.dataingesterlimiter import data_ingester_limiter

rate_limiter = data_ingester_limiter(current_app)
edgar_blueprint = Blueprint("edgar", __name__, url_prefix="/edgar", template_folder="templates")


@edgar_blueprint.route("/")
def edgar_index() -> str:
    return render_template("index.html")


@edgar_blueprint.route("/<ticker>")
@rate_limiter.limit(NINE_A_SECOND)
def edgar_ticker(ticker: str) -> str:
    return EDGARIngester().ingest(ticker)

from ingester_app.blueprints.edgar.models.cik_ticker_mapping import CikTickerMapping  # noqa