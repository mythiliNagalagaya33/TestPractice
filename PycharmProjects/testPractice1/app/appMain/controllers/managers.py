import uuid
from datetime import timedelta

from flask import request
from flask_jwt_extended import create_access_token
from flask_restx import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from app.appMain import db
from app.appMain.dto.managers import ManagerDto
from app.appMain.models.managers import Manager
from app.appMain.services.managers import ManagerService

manager_blueprint = ManagerDto.manager



@manager_blueprint.route('/signUp', methods=['POST'])
class Signup(Resource):
    def post(self):
        data=request.get_json()
        return ManagerService.signUp(data)



@manager_blueprint.route('/login', methods=['POST'])
class Login(Resource):
    def post(self):
        data=request.get_json()
        return ManagerService.login(data)


