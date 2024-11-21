import uuid

from sqlalchemy import Column, ForeignKey, UUID
from sqlalchemy.orm import relationship
# from sqlalchemy.dialects.postgresql import UUID as PGUUID
from app.appMain import db


class Listings(db.Model):
    __tablename__ = 'listings'

    listing_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    service_id = db.Column(UUID(as_uuid=True), db.ForeignKey('localservices.service_id'), nullable=False)
    provider_id =db.Column(UUID(as_uuid=True), db.ForeignKey('service_provider.provider_id'), nullable=False)

    local_services = db.relationship('LocalServices', back_populates='listings')  # One-to-Many relationship
    providers = db.relationship('Provider', back_populates='listings')  # One-to-Many relationship


# listing = db.Table(
#     'listings',
#     db.Column('listing_id',UUID(as_uuid=True),primary_key=True),
#     db.Column('service_id', UUID(as_uuid=True), db.ForeignKey('localservices.service_id'), primary_key=True),
#     db.Column('provider_id', UUID(as_uuid=True), db.ForeignKey('service_provider.provider_id'), primary_key=True))