from app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class Inventory(db.Model):
    __tablename__ = 'inventory'

    inventory_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Inventory record's UUID, auto-generated
    item_id = db.Column(UUID(as_uuid=True), db.ForeignKey('items.item_id'), nullable=False)  # Foreign key to items table
    quantity = db.Column(db.Integer, nullable=False)  # Quantity added or removed
    action = db.Column(db.String(15), nullable=False)  # Action (added or removed)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)  # Record creation timestamp
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)  # Record update timestamp

    # Relationships
    item = db.relationship('Item', backref='inventory', lazy=True)  # Link to the related item

    def __init__(self, item_id, quantity, action, **kwargs):
        self.item_id = item_id
        self.quantity = quantity
        self.action = action
        super(Inventory, self).__init__(**kwargs)

    def to_dict(self):
        return {
            'inventory_id': str(self.inventory_id),  # Return UUID as string
            'item_id': str(self.item_id),
            'quantity': self.quantity,
            'action': self.action,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
