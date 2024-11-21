from flask_restx import Namespace

class AdminDto:
    admin = Namespace('admin', description='API for admin operations')