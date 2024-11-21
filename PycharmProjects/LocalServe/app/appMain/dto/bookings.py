from flask_restx import Namespace, fields

class BookingDto:
    bookings = Namespace('bookings', description='API for booking operations')