from flask_restx import Namespace, fields

class ListingsDto:
    listings = Namespace('listings', description='API for listings operations')