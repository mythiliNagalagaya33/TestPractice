from app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class Item(db.Model):
    __tablename__ = 'items'

    item_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Item's UUID, auto-generated
    item_name = db.Column(db.String(50), nullable=False)  # Name of the item
    item_price = db.Column(db.Integer, nullable=False)  # Price of the item
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('categories.category_id'), nullable=False)  # Foreign key to categories table
    description = db.Column(db.Text, nullable=False)  # Description of the item
    quantity = db.Column(db.Integer, nullable=False)  # Quantity of the item
    manager_id = db.Column(UUID(as_uuid=True), db.ForeignKey('managers.manager_id'), nullable=False)  # Foreign key to managers table
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)  # Creation timestamp
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)  # Update timestamp

    # Relationships
    category = db.relationship('Category', backref='items', lazy=True)
    manager = db.relationship('Manager', backref='items', lazy=True)

    def __init__(self, item_name, item_price, category_id, description, quantity, manager_id, **kwargs):
        self.item_name = item_name
        self.item_price = item_price
        self.category_id = category_id
        self.description = description
        self.quantity = quantity
        self.manager_id = manager_id
        super(Item, self).__init__(**kwargs)

    def to_dict(self):
        return {
            'item_id': str(self.item_id),  # Return UUID as string
            'item_name': self.item_name,
            'item_price': self.item_price,
            'category_id': str(self.category_id),
            'description': self.description,
            'quantity': self.quantity,
            'manager_id': str(self.manager_id),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
