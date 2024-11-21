import uuid
from datetime import datetime

from flask import request, jsonify, make_response
from flask_restx import Resource
from app.appMain import db
from app.appMain.controllers import city
from app.appMain.dto.admin import AdminDto
from app.appMain.models.admin import Admin  # Assuming Admin model exists
from app.appMain.models.service_providers import Provider
from app.appMain.models.users import User

admin_blueprint = AdminDto.admin


#
# @admin_blueprint.route('/login', methods=['POST'])
# class Login(Resource):
#     def post(self):
#         data = request.get_json()
#         email = data.get('email')
#         password = data.get('password')
#         admin = Admin.query.filter_by(email=email).first()
#         if admin and admin.verify_password(password):
#             return {'message': 'Login Success'}, 200
#         else:
#             return {'message': 'Login failed'}, 401


@admin_blueprint.route('/userslist', methods=['GET'])
class AdminUsers(Resource):
    def get(self):
        # email = request.args.get('email')
        # admin = Admin.query.filter_by(email=email).first()
        # if not admin:
        #     return {'message': 'Unauthorized'}, 401

        users = User.query.all()
        datalist=[]

        for user in users:
            user_data = {
                "user_id": user.user_id,
                "user_name": user.user_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "status": user.status,
                "city": user.city_id
            }
            datalist.append(user_data)

        return make_response(datalist,200)

@admin_blueprint.route('/edituser', methods=['PUT'])
class EditUser(Resource):
     def put(self):
         data = request.get_json()
         user = User.query.get('10c1b75a-3cf6-4c69-9843-01d649e7bcb9')

         user.user_name = data.get('user_name')
         user.email = data.get('email')
         user.phone_number = data.get('phone_number')
         # city_id = data.get('city_id')
         # if city_id:
         #     user.city_id = city_id  # Assuming city_id is a foreign key in User
         #
         db.session.commit()
         return make_response({'message': 'User updated successfully'}, 200)


@admin_blueprint.route('/providerlist', methods=['GET'])
class AdminProvider(Resource):
    def get(self):
        service_providers = Provider.query.all()
        datalist=[]

        for provider in service_providers:
            provider_data = {
                "provider_id": provider.provider_id,
                "provider_name": provider.provider_name,
                # "service_name": provider.service_name,
                "email": provider.email,
                "phone_number": provider.phone_number,
                "city": provider.city.name,
                "status":provider.status
            }
            datalist.append(provider_data)

        return make_response(datalist,200)

@admin_blueprint.route('/pending-providers', methods=['GET'])
class PendingProviders(Resource):
    def get(self):
        try:
            # Fetch all providers with a pending status
            pending_providers = Provider.query.filter_by(status='pending').all()

            if not pending_providers:
                return {'message': 'No pending providers found.'}, 200

            provider_data = []
            for provider in pending_providers:
                services = [listing.local_services.service_name for listing in provider.listings]
                provider_data.append({
                    'provider_id': str(provider.provider_id),
                    'provider_name': provider.provider_name,
                    'email': provider.email,
                    'phone_number': provider.phone_number,
                    'city_name': provider.city.to_dict()['name'] if provider.city else None,
                    'address': provider.address,
                    'service_names': services, # Include the list of service names
                    'qualification':provider.qualification,
                    'bio':provider.bio,
                    'experience':provider.experience
                })

            return {'pending_providers': provider_data}, 200

        except Exception as e:
            return {'message': 'An error occurred while fetching pending providers.', 'error': str(e)}, 500


@admin_blueprint.route('/approve-provider/<uuid:provider_id>', methods=['POST'])
class ApproveProvider(Resource):
    def post(self, provider_id):
        data = request.get_json()
        action = data.get('action')  # Expected values: 'approve' or 'reject'

        # Validate action
        if action not in ['approve', 'reject']:
            return {'message': 'Invalid action'}, 400

        # Fetch provider by ID
        provider = Provider.query.get(provider_id)
        if not provider:
            return {'message': 'Provider not found'}, 404

        # Check current status and update based on action
        if provider.status == 'pending':
            if action == 'approve':
                provider.status = 'Available'
                status_message = 'approved'
                return_message = 'Provider approved successfully.'
            else:
                provider.status = 'rejected'
                status_message = 'rejected'
                return_message = 'Sorry to inform you, your request has been rejected.'
        else:
            return {'message': 'Action not allowed. Provider status is already updated.'}, 400

        try:
            db.session.commit()
            return {'message': return_message}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': 'Error updating provider status', 'error': str(e)}, 500


@admin_blueprint.route('/toggle-user-status/<uuid:user_id>', methods=['PUT'])
class ToggleUserStatus(Resource):
    def put(self, user_id):
        try:
            # Fetch the user by ID
            user = User.query.get(user_id)
            if not user:
                return {'message': 'User not found'}, 404

            # Toggle the user status
            if user.status == 'active':
                user.status = 'inactive'
                status_message = 'User status updated to inactive successfully'
            else:
                user.status = 'active'
                status_message = 'User status updated to active successfully'

            # Commit the changes to the database
            db.session.commit()
            return {'message': status_message}, 200

        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            return {'message': 'Error toggling user status', 'error': str(e)}, 500



@admin_blueprint.route('/toggle-provider-status/<uuid:provider_id>', methods=['PUT'])
class ToggleProviderStatus(Resource):
    def put(self, provider_id):
        try:
            # Fetch the provider by ID
            provider = Provider.query.get(provider_id)  # Replace with your Provider model
            if not provider:
                return {'message': 'Provider not found'}, 404

            # Toggle the provider status
            if provider.status == 'Available':
                provider.status = 'Unavailable'
                status_message = 'Provider has been deactivated and is now Unavailable'
            else:
                provider.status = 'Available'
                status_message = 'Provider has been reactivated and is now Available'

            # Commit the changes to the database
            db.session.commit()
            return {'message': status_message}, 200

        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            return {'message': 'Error toggling provider status', 'error': str(e)}, 500




#
# @admin_blueprint.route('/approve-provider/<uuid:provider_id>', methods=['POST'])
# class ApproveProvider(Resource):
#     def post(self, provider_id):
#         data = request.get_json()
#         action = data.get('action')  # Expected values: 'approve' or 'reject'
#
#         # Validate action
#         if action not in ['approve', 'reject']:
#             return {'message': 'Invalid action'}, 400
#
#         # Fetch provider by ID
#         provider = Provider.query.get(provider_id)
#         if not provider:
#             return {'message': 'Provider not found'}, 404
#
#         # Check current status and update based on action
#         if provider.status == 'pending':
#             if action == 'approve':
#                 provider.status = 'Available'
#                 status_message = 'approved'
#                 return_message = 'Provider approved successfully.'
#             else:
#                 provider.status = 'rejected'
#                 status_message = 'rejected'
#                 return_message = 'Sorry to inform you, your request has been rejected.'
#         else:
#             return {'message': 'Action not allowed. Provider status is already updated.'}, 400
#
#         try:
#             db.session.commit()
#             return {'message': return_message}, 200
#         except Exception as e:
#             db.session.rollback()
#             return {'message': 'Error updating provider status', 'error': str(e)}, 500


# @admin_blueprint.route('/users/total', methods=['GET'])
# class TotalUsers(Resource):
#     def get(self):
#         total_users = User.query.count()
#         return make_response({'totalUsers': total_users}, 200)
#
# @admin_blueprint.route('/providers/total', methods=['GET'])
# class TotalProviders(Resource):
#     def get(self):
#         total_providers = Provider.query.count()
#         return make_response({'totalProviders': total_providers}, 200)



# @admin_blueprint.route('/delete', methods=['DELETE'])
# class DeleteAdmin(Resource):
#     def delete(self):
#         email = request.args.get('email')
#
#         if not email:
#             return {'message': 'Admin email is required'}, 400
#
#         admin = Admin.query.filter_by(email=email).first()
#         if admin:
#             db.session.delete(admin)
#             db.session.commit()
#             return {'message': 'Admin deleted successfully'}, 200
#         else:
#             return {'message': 'Admin not found'}, 404










# @admin_blueprint.route('/admin', methods=['GET'])
# class GetAdmin(Resource):
#     def get(self):
#         email = request.args.get('email')
#         if not email:
#             return {'message': 'Please provide a valid email'}, 400
#
#         admin = Admin.query.filter_by(email=email).first()
#         if not admin:
#             return {'message': 'Admin not found'}, 404
#
#         admin_data = {
#             "admin_id": admin.admin_id,
#             "username" : admin.username,
#             "email": admin.email,
#             "password" : admin.password_hash
#         }
#
#         return make_response(jsonify(admin_data), 200)



# @admin_blueprint.route('/signup', methods=['POST'])
# class Signup(Resource):
#     def post(self):
#         data = request.get_json()
#         print("Received data:", data)
#
#         existing_admin_email = Admin.query.filter_by(email=data['email']).first()
#         if existing_admin_email:
#             return {'message': 'Admin already exists'}, 400
#         #
        # new_admin = Admin(
        #     admin_id=str(uuid.uuid4()),
        #     username=data['username'],
        #     email=data['email'],
        #     created_at=datetime.now(),
        #     last_login=datetime.now()
        # )
        #
        # new_admin.password = data['password']
        # db.session.add(new_admin)
        # db.session.commit()
        #
        # return {'message': 'Successfully added admin'}, 201
