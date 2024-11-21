from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, DateTime


class Admin(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    last_login = db.Column(db.DateTime, nullable=True)


    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=10)

    def verify_password(self, password):
        # print(generate_password_hash('sh'))
        return check_password_hash(self.password_hash, password)