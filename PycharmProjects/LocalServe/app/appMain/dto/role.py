from flask_restx import Namespace

class RoleDto:
    rolenameapi = Namespace('role',description='API to get role name')

