from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# 1. On définit un petit modèle pour l'utilisateur dans la review
user_info_model = api.model('ReviewUser', {
    'first_name': fields.String,
    'last_name': fields.String
})

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# ... (garder review_update_model identique)

@api.route('/')
class ReviewList(Resource):
    # ... (garder post identique)

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews with user details"""
        reviews = facade.get_all_reviews()
        results = []
        for r in reviews:
            # ON RÉCUPÈRE L'UTILISATEUR VIA LA FACADE
            user = facade.get_user(r.user_id)
            results.append({
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user': {
                    'first_name': user.first_name if user else "Unknown",
                    'last_name': user.last_name if user else "User"
                }
            })
        return results, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID with user info"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        user = facade.get_user(review.user_id)
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user': {
                'first_name': user.first_name if user else "Unknown",
                'last_name': user.last_name if user else "User"
            },
            'place_id': review.place_id,
        }, 200

    # ... (garder put et delete identiques)