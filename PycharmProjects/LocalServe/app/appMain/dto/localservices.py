from flask_restx import Namespace


class LocalServicesDto:
    localservices= Namespace('localservices', description='API for service provider operations')

