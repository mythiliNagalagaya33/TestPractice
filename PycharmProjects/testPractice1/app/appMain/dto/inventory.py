from flask_restx import Namespace


class UserDto:
    inventories = Namespace('inventories', description='API to check inventories operations')


