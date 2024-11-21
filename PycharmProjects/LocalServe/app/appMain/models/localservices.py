from sqlalchemy import Column, String, Text, Numeric, Uuid
import uuid

from app.appMain import db


class LocalServices(db.Model):
    __tablename__ = 'localservices'

    service_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    pricing = db.Column(db.Numeric(10, 2), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    route = db.Column(db.String(255), nullable=True)
    # provider_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('service_provider.provider_id'), nullable=True)

    # providers = db.relationship('Provider', back_populates='local_services')  # Use the correct back reference name
    listings = db.relationship('Listings', back_populates='local_services')

    # provider = db.relationship('Provider', back_populates='local_services')

    def to_dict(self):
        # city_name = self.city.to_dict()['name'] if self.city else None  # Safely get city name

        result = {
            'service_id': str(self.service_id),
            'service_name': self.service_name,
            'description' : self.description,
            'pricing': str(self.pricing),
            'image_url':self.image_url

        }
        return result


