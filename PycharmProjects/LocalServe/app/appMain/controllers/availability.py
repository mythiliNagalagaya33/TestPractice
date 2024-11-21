from flask import jsonify, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource

from app.appMain import db
from app.appMain.dto.availability import AvailabilityDTO
from app.appMain.models.availability import Availability
from app.appMain.models.service_providers import Provider

availability_blueprint = AvailabilityDTO.availability


@availability_blueprint.route('/addavailability', methods=['POST'])
class CreateAvailability(Resource):
    @jwt_required()
    def post(self):
        data = request.json
        provider_id = get_jwt_identity()

        provider = Provider.query.filter_by(provider_id=provider_id).first()
        if not provider:
            return {"message": "Provider not found"}, 404

        existing_availability = Availability.query.filter_by(provider_id=provider_id, date=data['date']).first()
        if existing_availability:
            return {"message": "Availability for this date already exists, please choose another date"}, 400

        new_availability = Availability(
            provider_id=provider_id,
            date=data['date'],
            status= 'Available'
        )

        db.session.add(new_availability)
        db.session.commit()

        return make_response(new_availability.to_dict(), 201)



# @availability_blueprint.route('/<uuid:provider_id>/availabilities', methods=['GET'])
# class ProviderAvailabilities(Resource):
#     def get(self, provider_id):
#         print(provider_id)
#         """Get all availability records for a specific provider."""
#         availabilities = Availability.query.filter_by(provider_id=provider_id).all()
#         if not availabilities:
#             return {"message": "No availabilities found for this provider"}, 404
#         availability_list=[availability.to_dict() for availability in availabilities]
#         return make_response(availability_list, 200)


@availability_blueprint.route('/myavailabilities', methods=['GET'])
class ProviderAvailabilities(Resource):
    @jwt_required()
    def get(self):
        provider_id = get_jwt_identity()

        availabilities = Availability.query.filter_by(provider_id=provider_id).all()
        if not availabilities:
            return {"message": "No availabilities found. Please add availability."}, 404

        availability_list = [availability.to_dict() for availability in availabilities]
        return make_response(availability_list, 200)

@availability_blueprint.route('/deleteavailability/<uuid:availability_id>', methods=['DELETE'])
class DeleteAvailability(Resource):
    @jwt_required()
    def delete(self, availability_id):
        provider_id = get_jwt_identity()

        # Fetch the availability record by ID and provider_id
        availability = Availability.query.filter_by(availability_id=availability_id, provider_id=provider_id).first()
        if not availability:
            return {"message": "Availability not found or you do not have permission to delete this record."}, 404

        # Delete the availability
        db.session.delete(availability)
        db.session.commit()

        return make_response({"message": "Availability deleted successfully."}, 200)
