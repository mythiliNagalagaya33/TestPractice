from flask_restx import Namespace

class NotificationDto:
    notification = Namespace('notification',description='API to get role name')

