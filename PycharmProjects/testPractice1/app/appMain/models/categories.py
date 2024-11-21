from app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, TIMESTAMP
from datetime import datetime

class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Automatically generate a UUID for each category
    category_name = db.Column(db.String(50), nullable=False)  # Name of the category
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)  # Timestamp when the category is created
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp when the category is updated

    def __init__(self, category_name, **kwargs):
        self.category_name = category_name
        super(Category, self).__init__(**kwargs)

    # def to_dict(self):
    #     return {
    #         'category_id': str(self.category_id),  # Return the UUID as a string
    #         'category_name': self.category_name,
    #         'created_at': self.created_at,
    #         'updated_at': self.updated_at
    #     }
