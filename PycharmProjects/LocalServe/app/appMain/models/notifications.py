import uuid
from sqlalchemy import Column, UUID, String, TIMESTAMP, ForeignKey
from app.appMain import db

class Notification(db.Model):
    __tablename__ = 'notifications'

    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Random UUID as primary key
    sender_id = Column(UUID(as_uuid=True), nullable=True)  # Foreign key to sender (user)
    receiver_id = Column(UUID(as_uuid=True), nullable=True)  # Foreign key to receiver (user)
    notification_title = Column(String(255), nullable=False)  # Title of the notification
    is_read = Column(db.Boolean, nullable=False, default=False)  # Status of whether the notification is read
    description = Column(String, nullable=True)  # Description of the notification
    created_at = Column(TIMESTAMP, nullable=False, server_default=db.func.current_timestamp())  # Timestamp for creation

    def __init__(self,notification_id=None, sender_id=None, receiver_id=None, notification_title=None, description=None, **kwargs):
        self.notification_id = notification_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.notification_title = notification_title
        self.description = description
        super(Notification, self).__init__(**kwargs)

    def to_dict(self):
        return {
            'notification_id': str(self.notification_id),
            'sender_id': str(self.sender_id) if self.sender_id else None,
            'receiver_id': str(self.receiver_id) if self.receiver_id else None,
            'notification_title': self.notification_title,
            'description': self.description,
            'created_at': str(self.created_at.isoformat()),
            'is_read': self.is_read
        }
