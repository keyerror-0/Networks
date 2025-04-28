from datetime import datetime
from app import db

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<URL {self.url}>'