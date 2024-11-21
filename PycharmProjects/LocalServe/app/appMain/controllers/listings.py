

from flask import jsonify
from flask_restx import Resource

from app.appMain import db
from app.appMain.dto import listings
from app.appMain.dto.listings import ListingsDto
from app.appMain.models.listings import Listings
from app.appMain.models.localservices import LocalServices
from app.appMain.models.reviews import Review
from app.appMain.models.service_providers import Provider

listings_blueprint=ListingsDto.listings


@listings_blueprint.route('/services/providers', methods=['GET'])
class AllServicesAndProviders(Resource):
    def get(self):
        # Query to get all services and their associated providers
        services = db.session.query(listings.c.service_id, listings.c.provider_id).all()


        # Structuring the response
        services_providers = {}
        for service_id, provider_id in services:
            service_id_str = str(service_id)
            provider_id_str = str(provider_id)
            if service_id_str not in services_providers:
                services_providers[service_id_str] = {
                    "providers": []
                }
            services_providers[service_id_str]["providers"].append(provider_id_str)

        return jsonify(services_providers)


@listings_blueprint.route('/provider/<uuid:provider_id>/services',methods=['GET'])
class ProviderServices(Resource):
    def get(self, provider_id):
        services = db.session.query(listings.c.service_id).filter(listings.c.provider_id == provider_id).all()

        return jsonify([str(service_id) for service_id, in services])

# Resource for Service Providers
@listings_blueprint.route('/service/<uuid:service_id>/providers',methods=['GET'])
class ServiceProviders(Resource):
    def get(self, service_id):
        # providers = db.session.query(listings.c.provider_id).filter(listings.c.service_id == service_id).all()
        service_details = db.session.query(
            LocalServices,  # service details
            Provider,  # provider details
            Review  # reviews related to the service-provider pair
        ).join(
            Listings, Listings.service_id == service_id  # Join Listings with LocalService on service_id
        ).join(
            Provider, Provider.provider_id == Listings.provider_id  # Join Listings with Providers on provider_id
        ).join(
            Review, Review.listing_id == Listings.listing_id  # Join Reviews with Listings on listing_id
        ).all()
        print(service_details.Review.to_dict())
        # return jsonify([str(provider_id) for provider_id, in providers])




@listings_blueprint.route('/listing/<uuid:listing_id>', methods=['GET'])
class ListingServiceProvider(Resource):
    def get(self, listing_id):
        listing = db.session.query(Listings.service_id, Listings.provider_id).filter(Listings.listing_id == listing_id).first()

        # If listing is not found, return 404
        if not listing:
            return jsonify({"message": "Listing not found"}), 404

        # Structuring the response
        response = {
            "service_id": str(listing.service_id),
            "provider_id": str(listing.provider_id)
        }

        return jsonify(response)


