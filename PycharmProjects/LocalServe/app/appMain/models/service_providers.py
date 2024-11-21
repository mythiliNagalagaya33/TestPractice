
from sqlalchemy import Column,Enum ,String, Text, Uuid, ForeignKey, UUID
from sqlalchemy import Enum

import uuid

from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash

from app.appMain import db
from app.appMain.models.localservices import LocalServices


class Provider(db.Model):
    __tablename__ = 'service_provider'

    provider_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column('password',db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    city_id = db.Column(UUID(as_uuid=True), db.ForeignKey('city.city_id'), nullable=False)
    address = db.Column(db.String, nullable=False)
    status = db.Column(db.String, default='pending')  # New status field
    qualification = db.Column(db.String)
    bio = db.Column(db.String)  # Bio column
    experience = db.Column(db.String)

    city = db.relationship('City', backref='providers')
    # role = db.relationship('Role', backref='provider')  # Link to Role
    # local_services = db.relationship('LocalServices', back_populates='providers')  # One-to-Many relationship
    listings = db.relationship('Listings', back_populates='providers')

    # availabilities = db.relationship('Availability', backref='service_provider')


    def __init__(self, **kwargs):
        super(Provider, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=10)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def to_dict(self):
        city_name = self.city.to_dict()['name'] if self.city else None  # Safely get city name

        result = {
            'provider_id': str(self.provider_id),
            'provider_name': self.provider_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'city_id': str(self.city.city_id) if self.city else None,  # Return city_id for updates
            'city_name': city_name,
            'address': self.address,
            'services': self.get_services(),
            'qualification': self.qualification,
            'bio':self.bio,
            'experience':self.experience
            # Fetch services from listings

            # 'availabilities': [availability.to_dict() for availability in self.availabilities]  # Convert availabilities

        }
        return  result

    def get_services(self):
        services = []
        for listing in self.listings:
            service = LocalServices.query.get(listing.service_id)
            if service:
                services.append(service.to_dict())
        return services


 # services = []
        # for listing in self.listings:
        #     service = LocalServices.query.get(listing.service_id)
        #     if service:
        #         services.append(service.to_dict())




