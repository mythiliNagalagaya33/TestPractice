from datetime import datetime
from flask_restx import Resource

from flask import request, jsonify, make_response

from app.appMain import db
from app.appMain.dto.reviews import ReviewDto
from app.appMain.models.bookings import Booking
from app.appMain.models.ratings import Rating
from app.appMain.models.reviews import Review

reviews_blueprint=ReviewDto.reviews

@reviews_blueprint.route('/add-review', methods=['POST'])
class Reviews(Resource):
    def post(self):
        data = request.get_json()
        print(f"Received data: {data}")
        # user_id = data.get('user_id')
        # listing_id = data.get('listing_id')
        booking_id = data.get('booking_id')  # Optional
        rating = data.get('rating')
        comment = data.get('comment', None)
        rating=Rating.query.filter_by(rating_value=rating).first()

        booking = Booking.query.filter_by(booking_id=booking_id).first()
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        existing_review = Review.query.filter_by(booking_id=booking_id).first()
        if existing_review:
            return jsonify({'error':'review already exists'})

        # Create a new review instance
        new_review = Review(
            user_id=str(booking.user_id),
            listing_id=booking.listing_id,
            booking_id=str(booking_id),
            rating_id=str(rating.rating_id),
            comment=comment,
            created_at=str(datetime.utcnow())
        )

        db.session.add(new_review)
        db.session.commit()

        return make_response(new_review.to_dict(), 201)

