from crypt import methods
from datetime import timedelta, datetime

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restx import Resource
import uuid

from click import password_option
from flask import request, jsonify,make_response
from flask_restx import Resource
from marshmallow.fields import Method
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash, check_password_hash
from app.appMain import db
from app.appMain.controllers import localservices
from app.appMain.dto.users import UserDto
from app.appMain.models.admin import Admin
from app.appMain.models.availability import Availability
from app.appMain.models.bookings import Booking, BookingStatus
from app.appMain.models.city import City
from app.appMain.models.listings import Listings
from app.appMain.models.localservices import LocalServices
from app.appMain.models.notifications import Notification
from app.appMain.models.reviews import Review
from app.appMain.models.service_providers import Provider
from app.appMain.models.users import User
from app.appMain.models.role import Role

from app.appMain.dto.service_providers import ServiceProviderDto

provider_blueprint = ServiceProviderDto.provider


@provider_blueprint.route('/signup', methods=['POST'])
class Signup(Resource):
    def post(self):
        data = request.get_json()

        # Check if the city exists
        city = City.query.filter_by(city_id=data.get('city_id')).first()
        if not city:
            return {'message': 'City not found'}, 400

        # Check for existing provider email
        existing_provider_email = Provider.query.filter_by(email=data['email']).first()
        if existing_provider_email:
            return {'message': 'Provider already exists'}, 400

        # Create a new provider
        new_id = str(uuid.uuid4())
        new_provider = Provider(
            provider_id=new_id,
            provider_name=data.get('provider_name'),
            email=data.get('email'),
            # password=generate_password_hash(data.get('password')),
            phone_number=data.get('phone_number'),
            city_id=city.city_id,
            address=data.get('address'),
            status='pending',
            qualification=data.get('qualification'),
            bio=data.get('bio'),
            experience=data.get('experience')
        )
        new_provider.password_hash =generate_password_hash( data.get('password'))

        db.session.add(new_provider)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error occurred while saving provider data', 'error': str(e)}, 500

        # Now create the listings
        service_ids = data.get('service_ids', [])
        if not service_ids:
            return {'message': 'At least one Service ID is required'}, 400

        listings = []
        for service_id in service_ids:
            # Ensure the service ID is valid
            service = LocalServices.query.filter_by(service_id=service_id).first()
            if not service:
                return {'message': f'Service ID {service_id} does not exist'}, 400

            # Create the listing
            listing = Listings(
                listing_id=str(uuid.uuid4()),
                service_id=service_id,
                provider_id=new_id
            )
            listings.append(listing)

        db.session.add_all(listings)



        try:
            db.session.commit()
            return {'message': 'Successfully added Service Provider and their services'}, 201

        except Exception as e:
            db.session.rollback()
            return {'message': 'Error occurred while saving listing data', 'error': str(e)}, 500



@provider_blueprint.route('/login', methods = ['POST'])
class Login(Resource):
    def post(self):
        data = request.get_json()


        if not data.get('email') or not data.get('password'):
            return {'message': 'Missing email or password'}, 400



        provider = Provider.query.filter_by(email=data['email']).first()
        if provider and check_password_hash(provider.password_hash, data['password']):
            print(provider.email)
            # jwt_token=create_access_token(identity=str(provider.provider_id),expires_delta=timedelta(days=1))
            # print(jwt_token)
            return {'message': 'Login Successful', 'role': 'Service Provider'}

        return {'message': 'Invalid credentials'}, 401


  # admin = Admin.query.filter_by(email=data['email']).first()
        # if admin and admin.verify_password(data.get('password')):
        #     return {'message': 'Login Successful', 'role': 'admin'}



@provider_blueprint.route('/getProvider', methods=['GET'])
class GetProvider(Resource):
    @jwt_required()
    def get(self):
        provider_id = get_jwt_identity()
        provider = Provider.query.filter_by(provider_id=provider_id).first()

        if not provider:
            return {'message': 'Provider not found'}, 404

        # Include related services through listings
        provider_data = provider.to_dict()

        # Fetch the services related to this provider through listings
        services = []
        listings = Listings.query.filter_by(provider_id=provider.provider_id).all()
        for listing in listings:
            service = LocalServices.query.get(listing.service_id)
            if service:
                services.append(service.to_dict())

        # Add services to the provider data
        provider_data['services'] = services

        return make_response(provider_data, 200)

# @provider_blueprint.route('/updateProvider', methods=['PUT'])
# class UpdateProvider(Resource):
#     @jwt_required()
#     def put(self):
#         provider_id = get_jwt_identity()
#         data = request.get_json()
#
#         provider = Provider.query.filter_by(provider_id=provider_id).first()
        #
        # if not provider:
        #     return {'message': 'Provider not found'}, 404
        #
        # # Update provider fields
        # provider.provider_name = data.get('provider_name', provider.provider_name)
        # provider.email = data.get('email', provider.email)
        # provider.phone_number = data.get('phone_number', provider.phone_number)
        # provider.address = data.get('address', provider.address)
        #
        # # Get the city based on the provided city_id
        # city = City.query.filter_by(name=data.get('city_name')).first()
        # if city:
        #     provider.city_id = city.city_id
        # else:
        #     return {'message': 'City not found'}, 404
        #
        # # Manage services
        # if 'services' in data:
        #     for service_id in data['services']:
        #         # Check if the service already exists
        #         existing_listing = Listings.query.filter_by(provider_id=provider.provider_id, service_id=service_id).first()
        #         if not existing_listing:
        #             # Create a new listing only if it doesn't exist
        #             listing = Listings(service_id=service_id, provider_id=provider.provider_id)
        #             db.session.add(listing)
        #
        # # Handle service deletions
        # if 'remove_services' in data:
        #     for service_id in data['remove_services']:
        #         listing = Listings.query.filter_by(provider_id=provider.provider_id, service_id=service_id).first()
        #         if listing:
        #             db.session.delete(listing)
        #
        # db.session.commit()
        # return {'message': 'Provider updated successfully', 'provider': provider.to_dict()}, 200

@provider_blueprint.route('/<uuid:provider_id>/availabilities', methods=['GET'])
class ProviderAvailabilities(Resource):
    def get(self, provider_id):
        print(provider_id)
        """Get all availability records for a specific provider."""
        availabilities = Availability.query.filter_by(provider_id=provider_id,status='Available').filter(Availability.date>=datetime.today().date()).all()
        print(1)
        listings = Listings.query.filter_by(provider_id=provider_id).all()
        print(2)

        reviews = []
        for listing in listings:
            review = Review.query.filter_by(listing_id=listing.listing_id).all()
            for r in review:
                reviews.append(r.to_dict())
        print(3)

        if not availabilities:
            return {"message": "No availabilities found for this provider"}, 404
        print(4)

        availability_list=[availability.to_dict() for availability in availabilities]
        print(reviews)
        provider_data = {
                "availability":availability_list,
                "Reviews":reviews,


        }
        print(6)

        return make_response(provider_data, 200)


@provider_blueprint.route('/pending_bookings')
class GetPendingBookings(Resource):
    @jwt_required()
    def get(self):
        provider_id = get_jwt_identity()  # Assuming the JWT identity is the provider's ID
        try:
            # Fetch pending bookings for the logged-in provider
            pending_bookings = (
                Booking.query
                .join(Listings, Booking.listing_id == Listings.listing_id)
                .filter(Listings.provider_id == provider_id, Booking.status == BookingStatus.PENDING)
                .all()
            )

            if not pending_bookings:
                return {"message": "No pending bookings found for this provider."}, 200

            return [booking.to_dict() for booking in pending_bookings], 200

        except Exception as e:
            return {"message": "An error occurred while fetching pending bookings.", "error": str(e)}, 500

@provider_blueprint.route('/confirmed_bookings')
class GetConfirmedBookings(Resource):
    @jwt_required()
    def get(self):
        # Fetch the provider ID from the JWT identity
        provider_id = get_jwt_identity()  # Ensure this returns the correct provider ID

        # Query confirmed bookings using the provider_id from Listings
        confirmed_bookings = (
            Booking.query
            .join(Listings, Booking.listing_id == Listings.listing_id)
            .filter(Listings.provider_id == provider_id, Booking.status == BookingStatus.CONFIRMED)
            .all()
        )

        # Check if any confirmed bookings were found
        if not confirmed_bookings:
            return {"message": "No confirmed bookings found."}, 200

        # Return the confirmed bookings in response
        return {
            "confirmed_bookings": [booking.to_dict() for booking in confirmed_bookings]
        }, 200


@provider_blueprint.route('/completed_bookings', methods=['GET'])
class GetCompletedBookings(Resource):
    @jwt_required()
    def get(self):
        # Fetch the provider ID from the JWT identity
        provider_id = get_jwt_identity()  # Ensure this returns the correct provider ID

        try:
            # Query completed bookings using the provider_id from Listings
            completed_bookings = (
                Booking.query
                .join(Listings, Booking.listing_id == Listings.listing_id)
                .filter(Listings.provider_id == provider_id, Booking.status == BookingStatus.COMPLETED)
                .all()
            )

            # Check if any completed bookings were found
            if not completed_bookings:
                return {"message": "No completed bookings found."}, 200

            # Return the completed bookings in response
            return {
                "completed_bookings": [booking.to_dict() for booking in completed_bookings]
            }, 200

        except Exception as e:
            return {"message": "An error occurred while fetching completed bookings.", "error": str(e)}, 500


@provider_blueprint.route('/getNotifications', methods=['GET'])
class GetNotifications(Resource):
    @jwt_required()
    def get(self):
        provider_id=get_jwt_identity()
        notifications = Notification.query.filter_by(receiver_id=provider_id)

        if not notifications:
            return {"message": "No notifications found."}, 200

        # Convert notifications to dictionary form to return as JSON
        notifications_list = [notification.to_dict() for notification in notifications]

        return make_response(notifications_list, 200)


@provider_blueprint.route('/markAllNotificationsAsRead', methods=['POST'])
class MarkAllNotificationsAsRead(Resource):
    @jwt_required()
    def post(self):
        provider_id = get_jwt_identity()

        # Fetch all unread notifications for the provider
        notifications = Notification.query.filter_by(receiver_id=provider_id, is_read=False).all()

        if not notifications:
            return {"message": "No unread notifications found for this provider."}, 404

        try:
            # Mark all notifications as read
            for notification in notifications:
                notification.is_read = True

            # Commit changes to the database
            db.session.commit()

            return {"message": "All notifications marked as read."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while updating notifications.", "error": str(e)}, 500




# @provider_blueprint.route('/markNotificationAsRead/<uuid:notification_id>', methods=['POST'])
# class MarkNotificationAsRead(Resource):
#     @jwt_required()
#     def post(self, notification_id):
#         provider_id = get_jwt_identity()
#
#         # Fetch the notification by ID and check if it's for the provider
#         notification = Notification.query.filter_by(notification_id=notification_id, receiver_id=provider_id).first()
#
#         if not notification:
#             return {"message": "Notification not found or not for this provider."}, 404
#
#         # Mark the notification as read if it is not already read
#         if not notification.is_read:
#             notification.is_read = True
#             db.session.commit()
#
#         return {"message": "Notification marked as read."}, 200
