import uuid
from datetime import datetime
from enum import unique

from sqlalchemy import UUID
from app.appMain import db



class Country(db.Model):
    __tablename__ = 'country'

    country_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Country, self).__init__(**kwargs)
