import uuid
from datetime import datetime
import app.appMain.models.state

from sqlalchemy import UUID
from app.appMain import db




class City(db.Model):
    __tablename__ = 'city'

    city_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = db.Column(db.String(100), nullable=False)
    postal_number = db.Column(db.String(20),unique=True, nullable=False)
    state_id = db.Column(UUID(as_uuid=True), db.ForeignKey('states.state_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    state=db.relationship('State',backref='cities')

    def __init__(self, **kwargs):
        super(City, self).__init__(**kwargs)

    def to_dict(self):
        return {
            'city_id': str(self.city_id),
            'name': self.name,
            'postal_number': self.postal_number,
            'state_id': str(self.state_id),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }