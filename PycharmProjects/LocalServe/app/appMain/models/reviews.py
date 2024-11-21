import uuid
from datetime import datetime

from sqlalchemy.orm import backref

from app.appMain import db
from app.appMain.models.bookings import Booking
from app.appMain.models.listings import Listings


class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.user_id'), nullable=False)  # Foreign key to users table
    listing_id = db.Column(db.UUID(as_uuid=True),db.ForeignKey(Listings.listing_id), nullable=False)  # Foreign key to listings table
    booking_id = db.Column(db.UUID(as_uuid=True),db.ForeignKey(Booking.booking_id), nullable=True)  # Foreign key to bookings table, optional
    rating_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('ratings.rating_id'), nullable=False)
    comment = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, nullable=False)

    # Relationship
    rating = db.relationship('Rating', backref='reviews')
    user = db.relationship('User', backref='users')



    def to_dict(self):
        return {
            'review_id': str(self.review_id),
            'user_name': self.user.user_name,
            'listing_id': str(self.listing_id),
            'booking_id': str(self.booking_id) if self.booking_id else None,
            'rating': self.rating.to_dict(),
            'comment': self.comment,
            'created_at':str( self.created_at.isoformat())
        }