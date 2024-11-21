from flask_restx import Namespace


class UserDto:
    user = Namespace('user', description='API for user operations')


