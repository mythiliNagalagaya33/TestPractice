from flask_restx import Namespace


class ServiceProviderDto:
    provider = Namespace('provider', description='API for service provider operations')



