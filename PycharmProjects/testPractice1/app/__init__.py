from flask import Blueprint
from flask_restx import Api

from app.appMain.controllers.items import item_blueprint
from app.appMain.controllers.managers import manager_blueprint

blueprint = Blueprint('api',__name__)
api = Api(blueprint, title='testPractice')

api.add_namespace(manager_blueprint)
api.add_namespace(item_blueprint)