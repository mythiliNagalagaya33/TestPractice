
import uuid
from datetime import timedelta

from flask import request, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restx import Resource
from werkzeug.security import generate_password_hash, check_password_hash

from app.appMain import db
from app.appMain.dto.items import ItemDto
from app.appMain.dto.managers import ManagerDto
from app.appMain.models.categories import Category
from app.appMain.models.items import Item
from app.appMain.models.managers import Manager

item_blueprint = ItemDto.items

# Api to add item
@item_blueprint.route('/addItems', methods=['POST'])
class AddItem(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        manager_id=get_jwt_identity()
        category = Category.query.filter_by(category_id=data.get('category_id')).first()

        if not category:
            return {'message': 'Invalid category ID'}, 400

        new_item = Item(
            item_id=str(uuid.uuid4()),
            item_name=data.get('item_name'),
            item_price=data.get('item_price'),
            category_id=data.get('category_id'),
            description=data.get('description'),
            quantity=data.get('quantity'),
            manager_id=manager_id  # Manager ID from JWT
        )

        db.session.add(new_item)
        db.session.commit()

        return {'message': 'Item added successfully', 'item': new_item.to_dict()}, 201

# api to get items
@item_blueprint.route('/items', methods=['GET'])
class GetItems(Resource):
    @jwt_required()
    def get(self):
        items = Item.query.filter_by(manager_id=get_jwt_identity()).all()
        items_list = [item.to_dict() for item in items]
        return make_response(items_list, 200)

# api to edit items
@item_blueprint.route('/editItem/<uuid:item_id>', methods=['PUT'])
class EditItem(Resource):
    @jwt_required()
    def put(self, item_id):
        data = request.get_json()
        item = Item.query.filter_by(item_id=item_id, manager_id=get_jwt_identity()).first()

        if not item:
            return {'message': 'Item not found or you do not have permission to edit this item'}, 404

        item.item_name = data.get('item_name', item.item_name)
        item.item_price = data.get('item_price', item.item_price)
        item.category_id = data.get('category_id', item.category_id)
        item.description = data.get('description', item.description)
        item.quantity = data.get('quantity', item.quantity)

        db.session.commit()

        return {'message': 'Item updated successfully'}, 200


@item_blueprint.route('/deleteItems/<uuid:item_id>', methods=['DELETE'])
class DeleteItem(Resource):
    @jwt_required()
    def delete(self, item_id):
        item = Item.query.filter_by(item_id=item_id, manager_id=get_jwt_identity()).first()

        if not item:
            return {'message': 'Item not found or you do not have permission to delete this item'}, 404

        db.session.delete(item)
        db.session.commit()

        return {'message': 'Item deleted successfully'}, 200
