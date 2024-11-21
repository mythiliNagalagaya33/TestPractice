from flask import jsonify, make_response, request
from flask_restx import Resource

from app.appMain import db
from app.appMain.dto.localservices import LocalServicesDto
from app.appMain.models.listings import Listings
from app.appMain.models.localservices import LocalServices
from app.appMain.models.service_providers import Provider

localservices_blueprint=LocalServicesDto.localservices


@localservices_blueprint.route('/addservice', methods=['POST'])
class CreateService(Resource):
    def post(self):
        """Create a new service."""
        data = request.json
        existing_service = LocalServices.query.filter_by(service_name=data['service_name']).first()
        if existing_service:
            return make_response({
                "message": "Service already exists"
            }, 400)
        new_service = LocalServices(
            service_name=data['service_name'],
            description=data.get('description'),
            pricing=data['pricing'],
            image_url=data.get('image_url'),
            route=data.get('route')
        )

        # Add the new service to the database
        db.session.add(new_service)
        db.session.commit()

        return make_response({
            "message" : "successfully created a service"
        }, 201)



@localservices_blueprint.route('', methods=['GET'])
class GetServices(Resource):
    def get(self):
        services = LocalServices.query.all()
        service_list = []

        for service in services:
            service_data = {
                'service_id': str(service.service_id),
                'service_name': service.service_name,
                'description': service.description,
                'pricing': float(service.pricing),
                'image_url': service.image_url,
                'route': service.route
                # 'provider_id':service.provider_id
            #
            }
            service_list.append(service_data)

        return make_response(service_list, 200)


@localservices_blueprint.route('/<string:service_id>', methods=['GET'])
class GetService(Resource):
    def get(self, service_id):
        service_id = service_id.strip()  # Trim any whitespace/newline characters
        service = LocalServices.query.filter_by(service_id=service_id).first()
        if not service:
            return make_response({"message": "Service not found"}, 404)

        service_data = {
            'service_id': str(service.service_id),
            'service_name': service.service_name,
            'description': service.description,
            'pricing': float(service.pricing),
            'image_url': service.image_url,
            'route': service.route,
            # 'provider': service.provider_id

        }
        # print(service.provider_id)
        return make_response(service_data, 200)

@localservices_blueprint.route('/<string:service_id>/providers', methods=['GET'])
class GetServiceWithProviders(Resource):
    def get(self, service_id):
        # Fetch the specified service
        service = LocalServices.query.filter_by(service_id=service_id).first()
        if not service:
            return make_response({"message": "Service not found"}, 404)

        # Prepare service data
        service_data = {
            'service_id': str(service.service_id),
            'service_name': service.service_name,
            'description': service.description,
            'pricing': float(service.pricing),
            'image_url': service.image_url,
            'route': service.route
        }

        # Fetch associated providers from the Listings table
        listings = Listings.query.filter_by(service_id=service.service_id).all()
        provider_ids = {listing.provider_id for listing in listings}

        # Get provider details
        providers = Provider.query.filter(Provider.provider_id.in_(provider_ids)).all()
        provider_list = [{
            'provider_id': str(provider.provider_id),
            'provider_name': provider.provider_name,
            'email': provider.email,
            'phone_number': provider.phone_number,
            'address': provider.address,
            'status':provider.status
        } for provider in providers if provider.status == 'Available']

        # Add providers to the service data
        service_data['providers'] = provider_list

        return make_response(service_data, 200)



#
# @localservices_blueprint.route('/deleteservice/<string:service_id>', methods=['DELETE'])
# class DeleteService(Resource):
#     def delete(self, service_id):
#         """Delete a service by its ID."""
#         service = LocalServices.query.filter_by(service_id=service_id).first()
#
#         if not service:
#             return make_response({
#                 "message": "Service not found"
#             }, 404)
#
#         # If the service exists, delete it
#         db.session.delete(service)
#         db.session.commit()
#
#         return make_response({
#             "message": "successfully deleted the service"
#         }, 200)

    # @localservices_blueprint.route('/updateservice/<string:service_id>', methods=['PUT'])
    # class UpdateService(Resource):
    #     def put(self, service_id):
    #         """Update an existing service."""
    #         data = request.json
    #         service = LocalServices.query.filter_by(service_id=service_id).first()
    #
    #         if not service:
    #             return make_response({
    #                 "message": "Service not found"
    #             }, 404)
    #
    #         # Update service fields
    #         service.service_name = data.get('service_name', service.service_name)
    #         service.description = data.get('description', service.description)
    #         service.pricing = data.get('pricing', service.pricing)
    #         service.image_url = data.get('image_url', service.image_url)  # Update image URL if provided
    #         service.route = data.get('route', service.route)  # Update route if provided
    #
    #         db.session.commit()
    #
    #         return make_response({
    #             "message": "Successfully updated the service"
    #         }, 200)