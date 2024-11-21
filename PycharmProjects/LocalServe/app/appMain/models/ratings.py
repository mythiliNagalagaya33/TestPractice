import uuid

from app.appMain import db


class Rating(db.Model):
    __tablename__ = 'ratings'

    rating_id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rating_value = db.Column(db.Integer, nullable=False, unique=True)  # Value from 1 to 5
    description = db.Column(db.String(100), nullable=True)  # Optional description (e.g., 'Excellent', 'Good')

    def to_dict(self):
        return {
            'rating_id': str(self.rating_id),
            'rating_value':str( self.rating_value),
            'description': self.description
        }