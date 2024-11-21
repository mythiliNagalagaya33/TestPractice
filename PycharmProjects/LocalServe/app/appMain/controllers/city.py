from crypt import methods

from flask import Flask, jsonify
from flask_restx import Resource
from flask_sqlalchemy import SQLAlchemy

from app.appMain.dto.city import CityDto
from app.appMain.models.city import City

city_blueprint=CityDto.cities


@city_blueprint.route('')
class CityList(Resource):
    def get(self):
        try:
            cities = City.query.all()
            return [city.to_dict() for city in cities], 200  # Return a list directly
        except Exception as e:
            return {'error': str(e)}, 500  # Return a dict directly

