import uuid
from datetime import timedelta

from click import password_option
from flask import request, jsonify,make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restx import Resource
from marshmallow.fields import Method
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash, check_password_hash
from app.appMain import db
from app.appMain.dto.users import UserDto
from app.appMain.models.admin import Admin
from app.appMain.models.bookings import Booking
from app.appMain.models.city import City
from app.appMain.models.listings import Listings
from app.appMain.models.notifications import Notification
from app.appMain.models.service_providers import Provider
from app.appMain.models.users import User
from app.appMain.models.role import Role


user_blueprint = UserDto.user

@user_blueprint.route('/signup', methods = ['POST'])
class Signup(Resource):
    def post(self):
        data = request.get_json()

        print("Received data:", data)
        city = City.query.filter_by(city_id=data.get('city_id')).first()
        print(city)

        existing_user_email = User.query.filter_by(email = data['email']).first()
        if existing_user_email:
            return {'message' : 'User already exists'}, 400

        new_user = User(
            user_id=str(uuid.uuid4()),
            user_name=data.get('user_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number'),
            street_address=data.get('street_address'),
            city_id=data.get('city_id'),
            role_id=data.get('role_id')
            # role=data.get('role')
        )
        new_user.password =data.get('password')
        db.session.add(new_user)
        db.session.commit()

        return {
            'message': 'successfully added user'
        }


@user_blueprint.route('/login', methods=['POST'])
class Login(Resource):
    def post(self):
        data = request.get_json()

        if not data.get('email') or not data.get('password'):
            return {'message': 'Missing email or password'}, 400

        # Check if the user is an Admin
        admin = Admin.query.filter_by(email=data['email']).first()
        if admin and admin.verify_password(data.get('password')):
            jwt_token = create_access_token(identity=str(admin.admin_id), expires_delta=timedelta(days=1))
            return {'message': 'Login Successful', 'role': 'admin', 'token': jwt_token}, 200

        # Check if the user exists in both Provider and User tables
        provider = Provider.query.filter_by(email=data['email']).first()
        user1 = User.query.filter_by(email=data['email']).first()

        if provider and user1:
            # Check if the password matches for both roles
            if not check_password_hash(provider.password_hash, data.get('password')) or \
               not check_password_hash(user1.password_hash, data.get('password')):
                return {'message': 'Invalid credentials'}, 401

            # Return a message indicating both roles are available
            provider_token = create_access_token(identity=str(provider.provider_id), expires_delta=timedelta(days=1))
            user_token = create_access_token(identity=str(user1.user_id), expires_delta=timedelta(days=1))

            # Return a message indicating both roles are available along with tokens
            return {
                'message': 'Multiple roles found. Please choose your role for login.',
                'roles': [
                    {'role': 'provider', 'token': provider_token},
                    {'role': 'user', 'token': user_token}
                ]
            }, 200

        # If only a Provider exists
        if provider:
            if provider.status == 'pending':
                return {'message': 'Your request is pending. Please wait for a few more days until it is approved.'}, 403

            if check_password_hash(provider.password_hash, data.get('password')):
                jwt_token = create_access_token(identity=str(provider.provider_id), expires_delta=timedelta(days=1))
                return {'message': 'Login Successful', 'role': 'provider', 'token': jwt_token}, 200

        # If only a User exists
        if user1:
            if user1.status == 'inactive':
                return {'message': 'Your account is in deactivate mode. Please contact admin for further details.'}, 404

            if check_password_hash(user1.password_hash, data.get('password')):
                jwt_token = create_access_token(identity=str(user1.user_id), expires_delta=timedelta(days=1))
                return {'message': 'Login Successful', 'role': 'user', 'token': jwt_token}, 200

        # If no valid credentials match
        return {'message': 'Invalid credentials'}, 401


@user_blueprint.route('/updateUser', methods=['PUT'])
class UpdateUser(Resource):
    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        user = User.query.filter_by(user_id=user_id).first()
        print(user.user_name)
        city= City.query.filter_by(city_id=data['city_id']).first()
        print(city)
        if not user:
            return {'message': 'User not found'}, 404
        user.user_name = data.get('user_name', user.user_name)
        user.email = data.get('email', user.email)
        user.phone_number = data.get('phone_number', user.phone_number)
        user.street_address = data.get('street_address', user.street_address)
        user.city_id = city.city_id
        db.session.commit()
        return {'message': 'User updated successfully', 'user': user.to_dict()}, 200



@user_blueprint.route('/getUser', methods = ['GET'])
class GetUser(Resource):
    @jwt_required()
    def get(self):
        print(1)
        # email=request.get_json()['email']
        user_id = get_jwt_identity()
        user1 = User.query.filter_by(user_id=user_id).first()
        print(1)
        if user1 is None:
            return {'message': 'User not found'}, 404
        return make_response(user1.to_dict(), 200)




@user_blueprint.route('/delete', methods= ['DELETE'])
class DeleteUser(Resource):
    def delete(self):
        email = request.args.get('email')

        if not email:
            return{'message' : 'User email is required'}, 400


        user = User.query.filter_by(email = email).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message' : 'user deleted successfully'}


        else:
            return{'message' : 'User not found'}, 404



@user_blueprint.route('/my_bookings')
class GetUserBookings(Resource):
    @jwt_required()
    def get(self):
        try:
            user_id = get_jwt_identity()
            user_bookings = Booking.query.filter_by(user_id=user_id).all()

            user_bookings_list =[]

            if not user_bookings:
                return {"message": "No bookings found for this user."}, 404

            for i in user_bookings:

                booked_data = {
                    'booking_id':i.to_dict()['booking_id'],
                    'user':i.to_dict()['user'],
                    'listing_id':i.to_dict()['listing_id'],
                    'availability':i.to_dict()['availability'],
                    'service':i.to_dict()['service'],
                    'booking_date':i.to_dict()['booking_date'],
                    'status':i.to_dict()['status']
                }
                user_bookings_list.append(booked_data)


                # user_bookings_list.append(i.to_dict())
                avail = i.to_dict()['availability']
                print(avail)

            return make_response(user_bookings_list, 200)

        except Exception as e:
            return {"message": "An error occurred while fetching user bookings.", "error": str(e)}, 500

@user_blueprint.route('/getNotifications', methods=['GET'])
class GetNotifications(Resource):
    @jwt_required()
    def get(self):
        user_id=get_jwt_identity()
        notifications = Notification.query.filter_by(receiver_id=user_id)

        if not notifications:
            return {"message": "No notifications found."}, 200

        # Convert notifications to dictionary form to return as JSON
        notifications_list = [notification.to_dict() for notification in notifications]

        return make_response(notifications_list, 200)

@user_blueprint.route('/markAllNotificationsAsRead', methods=['POST'])
class MarkAllNotificationsAsRead(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        # Fetch all unread notifications for the provider
        notifications = Notification.query.filter_by(receiver_id=user_id, is_read=False).all()

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

@user_blueprint.route('/getProvider/<uuid:listing_id>', methods=['GET'])
class GetProviderDetails(Resource):
    def get(self,listing_id):
        listings = Listings.query.filter_by(listing_id=listing_id)




# @user_blueprint.route('/login', methods = ['POST'])
# class Login(Resource):
#     def post(self):
#         data = request.get_json()
#         print(data)
#
#         if not data.get('email') or not data.get('password'):
#             return {'message': 'Missing email or password'}, 400
#
#         admin = Admin.query.filter_by(email=data['email']).first()
#         if admin and admin.verify_password(data.get('password')):
#             jwt_token = create_access_token(identity=str(admin.admin_id), expires_delta=timedelta(days=1))
#             return {'message': 'Login Successful', 'role': 'admin', 'token':jwt_token}, 200

        # provider = Provider.query.filter_by(email=data['email']).first()
        # if provider:
        #     # Check if the provider's status is pending
        #     if provider.status == 'pending':
        #         return {
        #             'message': 'Your request is pending. Please wait for a few more days until it is approved.'}, 403
        #
        #     if check_password_hash(provider.password_hash, data.get('password')):
        #         jwt_token = create_access_token(identity=str(provider.provider_id), expires_delta=timedelta(days=1))
        #         print(jwt_token)
        #         return {'message': 'Login Successful', 'role': 'provider', 'token': jwt_token}, 200


        # user1 = User.query.filter_by(email=data['email']).first()
        # if user1:
        #     # Check if the provider's status is pending
        #     if user1.status == 'inactive':
        #         return {
        #             'message': 'Your account is in deactivate mode please contact admin for further details'}, 404
        #
        # if user1 and check_password_hash(user1.password_hash, data['password']):
        #     jwt_token = create_access_token(identity=str(user1.user_id), expires_delta=timedelta(days=1))
        #     return {'message': 'Login Successful', 'role': 'user', 'token':jwt_token}, 200
        #
        # return {'message': 'Invalid credentials'}, 401
