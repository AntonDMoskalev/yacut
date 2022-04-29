from datetime import datetime

from . import db


class URL_map(db.Model):
    """
    The URL map model,
    for saving to the database about the original (long link)
    and the created short identifier,
    as well as the time of record creation.
    """
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(300), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)