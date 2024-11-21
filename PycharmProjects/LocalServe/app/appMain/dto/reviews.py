from flask_restx import Namespace

class ReviewDto:
    reviews = Namespace('reviews',description='API to get reviews name')

