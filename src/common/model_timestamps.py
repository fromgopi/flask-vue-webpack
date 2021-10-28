"""Timestamps for all models"""
from datetime import datetime
from app import DB


class TimestampMixin(object):
    created = DB.Column(DB.DateTime, nullable=False, default=datetime.utcnow)
    updated = DB.Column(DB.DateTime, onupdate=datetime.utcnow)