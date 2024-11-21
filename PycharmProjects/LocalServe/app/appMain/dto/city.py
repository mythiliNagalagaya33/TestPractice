from flask_restx import Namespace

class CityDto:
    cities = Namespace('cities',description='API to get cities')

