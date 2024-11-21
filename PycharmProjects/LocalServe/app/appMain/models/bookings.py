from enum import Enum

from sqlalchemy.orm import backref
from sqlalchemy.testing.suite.test_reflection import users

from app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID


class BookingStatus(Enum):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class Booking(db.Model):
    __tablename__ = 'bookings'

    booking_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)
    # provider_id = db.Column(UUID(as_uuid=True), db.ForeignKey('service_provider.provider_id'), nullable=False)
    # service_id = db.Column(UUID(as_uuid=True), db.ForeignKey('localservices.service_id'), nullable=False)
    listing_id = db.Column(UUID(as_uuid=True), db.ForeignKey('listings.listing_id'), nullable=False)
    booking_date = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())  # Date and time of booking
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.PENDING)
    # status = db.Column(db.String(50), nullable=False, default='pending')  # Default status to 'confirmed'
    availability_id = db.Column(UUID(as_uuid=True), db.ForeignKey('availability.availability_id'), nullable=False)  # New column



    user = db.relationship('User', backref='bookings')
    listings = db.relationship('Listings', backref='bookings')
    availability = db.relationship('Availability', backref='bookings')  # Relationship to availability

    # provider = db.relationship('Provider', backref='bookings')
    # service = db.relationship('LocalServices', backref='bookings')

    def __init__(self, user_id,listing_id, availability_id, **kwargs):
        self.user_id = user_id
        self.listing_id=listing_id
        self.availability_id = availability_id  # Set the availability_id

        # self.provider_id = provider_id
        # self.service_id = service_id
        super(Booking, self).__init__(**kwargs)

    def to_dict(self):
        """Return dictionary representation of the booking"""
        return {
            'booking_id': str(self.booking_id),  # Convert UUID to string
            'user': self.user.to_dict(),  # Convert UUID to string
            'listing_id':str(self.listing_id),
            # 'provider': self.listings.providers.to_dict(),
            'service':self.listings.local_services.to_dict(),
            # 'provider_id': str(self.provider_id),  # Convert UUID to string
            # 'service_id': str(self.service_id),  # Convert UUID to string
            'availability': self.availability.to_dict() if self.availability else None,  # Get availability details
            'booking_date': str(self.booking_date.isoformat()),  # ISO format for datetime
            'status': str(self.status.value)
        }

    def update_status(self, new_status):
        """Update booking status"""
        if new_status in ['confirmed', 'canceled']:
            self.status = new_status
        else:
            raise ValueError("Status must be 'confirmed' or 'canceled'")
