

from app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String



class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_name = db.Column(db.String(50), nullable=False)

    # users = db.relationship('User', back_populates='role')
    # service_providers = db.relationship('ProviderProfile', back_populates='role')