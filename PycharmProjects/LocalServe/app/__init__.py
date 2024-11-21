from flask import Blueprint
from flask_restx import Api

from app.appMain.controllers.admin import admin_blueprint
from app.appMain.controllers.availability import availability_blueprint
from app.appMain.controllers.bookings import booking_blueprint
from app.appMain.controllers.city import city_blueprint
from app.appMain.controllers.listings import listings_blueprint
# from app.appMain.controllers.listings import listings_blueprint
from app.appMain.controllers.localservices import localservices_blueprint
from app.appMain.controllers.reviews import reviews_blueprint
from app.appMain.controllers.service_provider import provider_blueprint
from app.appMain.controllers.users import user_blueprint

blueprint = Blueprint('api',__name__)
api = Api(blueprint, title='Mythili')
api.add_namespace(user_blueprint)
api.add_namespace(admin_blueprint)
api.add_namespace(provider_blueprint)
api.add_namespace(localservices_blueprint)
api.add_namespace(city_blueprint)
api.add_namespace(booking_blueprint)
api.add_namespace(listings_blueprint)
api.add_namespace(availability_blueprint)
api.add_namespace(reviews_blueprint)
