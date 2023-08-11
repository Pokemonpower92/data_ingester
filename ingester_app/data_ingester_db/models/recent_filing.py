from ingester_app import db


class RecentFiling(db.Model):

    __tablename__ = "recent_filing"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cik_str = db.Column(db.String(128), nullable=False)
    accessionNumber = db.Column(db.String(128))
    filingDate = db.Column(db.DateTime)
    reportDate = db.Column(db.DateTime)
    acceptanceDateTime = db.Column(db.DateTime)
    act = db.Column(db.String(128))
    form = db.Column(db.String(128))
    fileNumber = db.Column(db.String(128))
    filmNumber = db.Column(db.String(128))
    items = db.Column(db.String(128))
    size = db.Column(db.String(128))
    isXBRL = db.Column(db.Integer)
    isInlineXBRL = db.Column(db.Integer)
    primaryDocument = db.Column(db.String(128))
    primaryDocDescription = db.Column(db.String(128))

    def __init__(self, cik_str, **kwargs):
        self.cik_str = cik_str
        self.__dict__.update(kwargs)
