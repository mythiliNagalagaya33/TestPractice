from flask_restx import Namespace

class AvailabilityDTO:
    availability = Namespace('availability', description='API for availability operations')