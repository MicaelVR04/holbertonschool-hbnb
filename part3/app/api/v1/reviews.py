from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'user_id': fields.String(description='ID of the user writing the review (ignored, taken from token)')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)')
})

review_output_model = api.model('ReviewOutput', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating'),
    'place_id': fields.String(description='Place ID'),
    'user_id': fields.String(description='User ID'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    @api.marshal_list_with(review_output_model)
    def get(self):
        reviews = facade.get_all_reviews()
        return reviews, 200

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.marshal_with(review_output_model, code=201)
    def post(self):
        review_data = api.payload
        current_user = get_jwt_identity()

        place = facade.get_place(review_data['place_id'])
        if not place:
            api.abort(404, f"Place with ID {review_data['place_id']} not found")

        place_owner_id = getattr(place, 'owner_id', None)
        if not place_owner_id and getattr(place, 'owner', None):
            place_owner_id = getattr(place.owner, 'id', None)

        if place_owner_id == current_user:
            api.abort(400, "You cannot review your own place.")

        existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
        for r in existing_reviews:
            review_user_id = getattr(r, 'user_id', None)
            if not review_user_id and getattr(r, 'user', None):
                review_user_id = getattr(r.user, 'id', None)
            if review_user_id == current_user:
                api.abort(400, "You have already reviewed this place.")

        review_data['user_id'] = current_user

        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            api.abort(400, str(e))

        if not new_review:
            api.abort(400, 'Failed to create review')

        return new_review, 201


@api.route('/<string:review_id>')
class ReviewDetail(Resource):
    @api.doc('get_review')
    @api.marshal_with(review_output_model)
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Review {review_id} not found")
        return review, 200

    @jwt_required()
    @api.expect(review_update_model, validate=True)
    @api.marshal_with(review_output_model)
    def put(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Review {review_id} not found")

        current_user = get_jwt_identity()
        review_user_id = getattr(review, 'user_id', None)
        if not review_user_id and getattr(review, 'user', None):
            review_user_id = getattr(review.user, 'id', None)

        if review_user_id != current_user:
            api.abort(403, "Unauthorized action")

        review_data = api.payload

        try:
            updated_review = facade.update_review(review_id, review_data)
        except ValueError as e:
            api.abort(400, str(e))

        if not updated_review:
            api.abort(400, 'Failed to update review')

        return updated_review, 200

    @jwt_required()
    @api.doc('delete_review')
    def delete(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Review {review_id} not found")

        current_user = get_jwt_identity()
        review_user_id = getattr(review, 'user_id', None)
        if not review_user_id and getattr(review, 'user', None):
            review_user_id = getattr(review.user, 'id', None)

        if review_user_id != current_user:
            api.abort(403, "Unauthorized action")

        success = facade.delete_review(review_id)
        if not success:
            api.abort(400, 'Failed to delete review')

        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<string:place_id>')
class PlaceReviews(Resource):
    @api.doc('get_place_reviews')
    @api.marshal_list_with(review_output_model)
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place {place_id} not found")

        reviews = facade.get_reviews_by_place(place_id)
        return reviews, 200
