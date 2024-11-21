from werkzeug.security import generate_password_hash, check_password_hash
from app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String


class Manager(db.Model):
    __tablename__ = 'managers'

    manager_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Unique identifier for the manager
    first_name = db.Column(db.String(50), nullable=False)  # Manager's first name
    last_name = db.Column(db.String(50))  # Manager's last name (optional)
    email = db.Column(db.String(50), unique=True, nullable=False)  # Manager's email (unique)
    password_hash = db.Column("password",db.String(300), nullable=False)
    phone_number = db.Column(db.Integer, nullable=True)  # Manager's phone number (optional)
    created_at = db.Column(db.TIMESTAMP, default=db.func.now())  # Timestamp when the manager is created
    updated_at = db.Column(db.TIMESTAMP, default=db.func.now(), onupdate=db.func.now())  # Timestamp when updated

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=10)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'manager_id': str(self.manager_id),  # Return the manager's UUID as a string
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone_number': self.phone_number
        }
