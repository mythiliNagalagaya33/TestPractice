import uuid
from datetime import datetime
from enum import unique
import app.appMain.models.country

from sqlalchemy import UUID
from app.appMain import db



class State(db.Model):
    __tablename__ = 'states'

    state_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = db.Column(db.String(100),unique=True, nullable=False)
    country_id = db.Column(UUID(as_uuid=True), db.ForeignKey('country.country_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


    country = db.relationship('Country', backref=db.backref('states', lazy=True))


    def __init__(self, **kwargs):
        super(State, self).__init__(**kwargs)