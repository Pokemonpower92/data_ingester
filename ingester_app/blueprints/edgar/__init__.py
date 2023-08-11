from flask import Blueprint, render_template, current_app, make_response, Response

from ingester_app.data_ingester.edgaringester import EDGARIngester
from ingester_app.data_ingester_config.limitconfig import NINE_A_SECOND
from ingester_app.data_ingester_limiter.dataingesterlimiter import data_ingester_limiter

rate_limiter = data_ingester_limiter(current_app)
edgar_blueprint = Blueprint("edgar", __name__, url_prefix="/edgar", template_folder="templates")


@edgar_blueprint.route("/")
def edgar_index() -> str:
    return render_template("index.html")

@edgar_blueprint.route("/companyfacts")
def edgar_companyfacts() -> str:
    company_facts = EDGARIngester().ingest_companyfacts_data()
    return "Company Facts"

@edgar_blueprint.route("/<ticker>")
@rate_limiter.limit(NINE_A_SECOND)
def edgar_ticker(ticker: str) -> Response:
    return make_response({"oopsie x3": "There was a wittle 404 x3B"}, 404)

