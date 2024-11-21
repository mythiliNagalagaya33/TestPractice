from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import backref

from app.appMain import db
import uuid

class Availability(db.Model):
    __tablename__ = 'availability'

    availability_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_id =db.Column(UUID(as_uuid=True), db.ForeignKey('service_provider.provider_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)  # Date when the provider is available
    status = db.Column(db.String(50), default='available')  # Can be 'available', 'booked', or 'in-progress'

    service_provider = db.relationship('Provider', backref='providers')

    def __init__(self, provider_id, date, status='available'):
        self.provider_id = provider_id
        self.date = date
        self.status = status

    def to_dict(self):
        print(1)
        return {
            'availability_id': str(self.availability_id),  # Convert UUID to string
            'provider': self.service_provider.to_dict() ,  # Fetch provider details
            'date': str(self.date),  # ISO format for date
            'status': self.status
        }
