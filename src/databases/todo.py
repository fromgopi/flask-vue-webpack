from datetime import datetime

from app.databases import db


class Todo(db.Document):
    title = db.StringField(required=True)
    completed = db.BooleanField(default=False)
    createdAt = db.DateTimeField(default=datetime.utcnow)
    meta = {'': ''}

