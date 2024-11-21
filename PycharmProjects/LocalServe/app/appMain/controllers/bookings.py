import uuid
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from app.appMain import db
from app.appMain.dto.bookings import BookingDto
from app.appMain.models.bookings import Booking, BookingStatus
from app.appMain.models.listings import Listings
from app.appMain.models.notifications import Notification
from app.appMain.models.service_providers import Provider
from app.appMain.models.users import User
from app.appMain.models.localservices import LocalServices

booking_blueprint = BookingDto.bookings

@booking_blueprint.route('')
class CreateBooking(Resource):
    @jwt_required()
    def post(self):
        """Create a new booking"""
        data = request.json
        user_id=get_jwt_identity()

        print(f"Received date for booking: {data['date']}")

        user = User.query.filter_by(user_id = user_id).first()

        listing = Listings.query.filter_by(service_id =data['service_id'],provider_id=data['provider_id']).first()
        service = LocalServices.query.filter_by(service_id=data['service_id']).first()
        print(listing)

        availability = Availability.query.filter_by(provider_id = data['provider_id'],date= data['date']).first()
        print(availability)

        if not availability:
            return {"message":"Please select from the available dates"}, 200
        # print(availability_id.to_dict())
        # Validate incoming data
        # required_fields = [ 'listing_id']
        # if not all(key in data for key in required_fields):
        #     return {"message": "Missing required fields."}, 400  # Do not use jsonify

        try:
            # Create a new booking instance
            new_booking = Booking(
                user_id=user_id,
                listing_id=listing.listing_id,
                availability_id=availability.availability_id,

            )
            # availability.status = "Unavailable"

            db.session.add(new_booking)
            print(23)
            db.session.commit()
            print(25)
            print(1)
            notification=Notification(
                notification_id=str(uuid4()),
                sender_id=user_id,
                receiver_id=listing.provider_id,
                notification_title="You have new Service Request",
                description=f"You have received a new booking request from {user.user_name} for {service.service_name}  service on {data['date']}. Please review and confirm the booking."
            )
            print(3)

            db.session.add(notification)
            print(notification)
            db.session.commit()
            print(5)
            return new_booking.to_dict(), 201

        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while creating the booking.", "error": str(e)}, 500






@booking_blueprint.route('/my_bookings')
class GetUserBookings(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            user_bookings = Booking.query.filter_by(user_id=user_id).all()

            if not user_bookings:
                return {"message": "No bookings found for this user."}, 404

            return [booking.to_dict() for booking in user_bookings], 200

        except Exception as e:
            return {"message": "An error occurred while fetching user bookings.", "error": str(e)}, 500

from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource
from app.appMain import db
from app.appMain.dto.bookings import BookingDto
from app.appMain.models.availability import Availability

booking_blueprint = BookingDto.bookings

@booking_blueprint.route('/providers_by_date')
class GetProvidersByDate(Resource):
    @jwt_required()
    def get(self):
        """Get providers based on availability date"""
        # Retrieve date from query parameters
        date = request.args.get('date')
        if not date:
            return {"message": "Date is required."}, 400

        try:
            # Fetch available providers for the given date
            availabilities = Availability.query.filter_by(date=date).all()
            if not availabilities:
                return {"message": "No providers available for this date."}, 404

            provider_ids = {availability.provider_id for availability in availabilities}
            providers = Provider.query.filter(Provider.provider_id.in_(provider_ids)).all()

            return [provider.to_dict() for provider in providers], 200

        except Exception as e:
            return {"message": "An error occurred while fetching providers.", "error": str(e)}, 500



@booking_blueprint.route('/providers_by_date')
class GetProvidersByDate(Resource):
    @jwt_required()
    def get(self):
        """Get providers based on availability date"""
        # Retrieve date from query parameters
        date = request.args.get('date')
        if not date:
            return {"message": "Date is required."}, 400

        try:
            # Fetch available providers for the given date
            availabilities = Availability.query.filter_by(date=date).all()
            if not availabilities:
                return {"message": "No providers available for this date."}, 404

            provider_ids = {availability.provider_id for availability in availabilities}
            providers = Provider.query.filter(Provider.provider_id.in_(provider_ids)).all()

            return [provider.to_dict() for provider in providers], 200

        except Exception as e:
            return {"message": "An error occurred while fetching providers.", "error": str(e)}, 500




@booking_blueprint.route('/update_booking_status/<uuid:booking_id>')
class UpdateBookingStatus(Resource):
    @jwt_required()
    def patch(self, booking_id):
        """Update booking status (pending -> confirmed -> completed or cancelled)"""
        provider_id = get_jwt_identity()  # Assuming providers use the same JWT mechanism
        provider = Provider.query.filter_by(provider_id=provider_id).first()
        data = request.json
        new_status = data.get('status').lower()  # Convert to lowercase to match the enum values

        # Ensure the status is one of the valid options from the BookingStatus enum values
        valid_statuses = [status.value for status in BookingStatus]
        if new_status not in valid_statuses:
            return {"message": "Invalid booking status."}, 400

        try:
            # Fetch the booking by ID and join with Listings to ensure the provider owns the booking
            booking = (
                Booking.query
                .join(Listings, Booking.listing_id == Listings.listing_id)
                .filter(Booking.booking_id == booking_id, Listings.provider_id == provider_id)
                .first()
            )

            if not booking:
                return {"message": "Booking not found or you're not authorized."}, 404

            availability = Availability.query.filter_by(availability_id = booking.availability_id).first()
            availability.status = 'Unavailable'
            db.session.commit()
            notification = Notification(
                notification_id=str(uuid4()),
                sender_id=provider_id,
                receiver_id=booking.user_id,
                notification_title='Booking Status!'
            )
            # description=''
            # feedback_link = f'http://localhost:4200/user/feedback/{booking.booking_id}'  # Replace with your actual Angular app's URL and route

            if booking.status == BookingStatus.PENDING and new_status == BookingStatus.CONFIRMED.value:
                booking.status = BookingStatus.CONFIRMED
                notification.description=f'Your booking with {provider.provider_name} has been confirmed. Thank you for choosing our services!'
                db.session.add(notification)
                db.session.commit()
            elif booking.status == BookingStatus.CONFIRMED and new_status == BookingStatus.COMPLETED.value:
                booking.status = BookingStatus.COMPLETED
                availability.status = 'Available'
                notification.description = f'''Thank you for using our services! Your booking with {provider.provider_name} is now complete. We hope you had a great experience. Feel free to leave feedback:/user/feedback/{booking.booking_id}  '''
                db.session.add(notification)
                db.session.commit()
                # db.session.add(description)
                # db.session.commit()

            elif booking.status == BookingStatus.PENDING and new_status == BookingStatus.CANCELLED.value:
                booking.status = BookingStatus.CANCELLED
                notification.description=f"We're sorry, but your booking request with { provider.provider_name }has been declined. Please check other available providers or try again later"
                db.session.add(notification)
                db.session.commit()

            else:
                return {"message": "Invalid status transition."}, 400

            # notification = Notification(
            #     notification_id=str(uuid4()),
            #     sender_id=provider_id,
            #     receiver_id=booking.user_id,
            #     notification_title='Booking Status!',
            #     description=description
            # )
            print(notification.description,'printing description')


            return {"message": f"Booking status updated to {new_status}."}, 200

        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while updating booking status.", "error": str(e)}, 500

# @booking_blueprint.route('/allbookings')
# class GetAllBookings(Resource):
#     def get(self):
#         """Get all bookings"""
#         try:
#             bookings = Booking.query.all()
#             # Return all bookings, Flask-RESTx will handle serialization
#             return [booking.to_dict() for booking in bookings], 200
#
#         except Exception as e:
#             return {"message": "An error occurred while fetching bookings.", "error": str(e)}, 500
