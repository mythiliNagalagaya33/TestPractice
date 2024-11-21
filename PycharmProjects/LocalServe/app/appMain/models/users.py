from werkzeug.security import generate_password_hash, check_password_hash

from app.appMain import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column("password",db.String(300), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    street_address = db.Column(db.String(255), nullable=True)
    city_id = db.Column(UUID(as_uuid=True), db.ForeignKey('city.city_id'), nullable=True)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.role_id'), nullable=True)
    status = db.Column(db.String(50), nullable=False)  # Corrected here
    role = db.relationship('Role', backref='users')
    city = db.relationship('City', backref='users')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=10)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        print(self.city.to_dict()['name'])
        city_name = self.city.to_dict()['name'] if self.city else None  # Safely get city name

        return {
            'user_id': str(self.user_id),
            'user_name': self.user_name,
            'email': self.email,
            'phone_number': self.phone_number,
            'street_address': self.street_address,
            'city_id': str(self.city.city_id) if self.city else None,  # Return city_id for updates
            'city_name': city_name
        }



