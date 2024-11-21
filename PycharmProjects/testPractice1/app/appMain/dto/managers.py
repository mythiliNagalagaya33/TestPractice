from flask_restx import Namespace


class ManagerDto:
    manager = Namespace('manager', description='API for manager operations')


