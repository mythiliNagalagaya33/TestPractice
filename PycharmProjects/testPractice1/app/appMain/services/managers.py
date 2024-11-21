import uuid
from datetime import timedelta

from flask import request
from flask_jwt_extended import create_access_token

from app.appMain import db
from app.appMain.models.managers import Manager


class ManagerService:
    @staticmethod
    def signUp(data):

        # Check if the manager already exists
        existing_manager = Manager.query.filter_by(email=data['email']).first()
        if existing_manager:
            return {'message': 'Manager already exists'}, 400

        # Create new manager
        new_manager = Manager(
            manager_id=str(uuid.uuid4()),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone_number=data.get('phone_number')
        )
        new_manager.password = data.get('password')  # This will trigger the setter to hash the password
        db.session.add(new_manager)
        db.session.commit()

        return {'message': 'Manager successfully registered'}, 201

    @staticmethod
    def login(data):
        data = request.get_json()

        if not data.get('email') or not data.get('password'):
            return {'message': 'Missing email or password'}, 400

        manager = Manager.query.filter_by(email=data['email']).first()
        if manager and manager.verify_password(data['password']):
            jwt_token = create_access_token(identity=str(manager.manager_id), expires_delta=timedelta(days=1))
            return {'message': 'Login successful', 'token': jwt_token}, 200

        return {'message': 'Invalid credentials'}, 401
