from flask_restx import Namespace


class ItemDto:
    items = Namespace('items', description='API for item operations')


