from ingester_app import db


class CikTickerMapping(db.Model):

    __tablename__ = "cik_ticker_mapping"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cik_str = db.Column(db.String(128), nullable=False)
    ticker = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(128), nullable=False)

    def __init__(self, cik_str, ticker, title, *args, **kwargs):
        self.cik_str = cik_str
        self.ticker = ticker
        self.title = title
