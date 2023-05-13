from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app import app
from app.data_ingester_config.limitconfig import NINE_A_SECOND, TWO_HUNDRED_A_DAY

data_ingester_limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[TWO_HUNDRED_A_DAY, NINE_A_SECOND],
    storage_uri="memory://",
)