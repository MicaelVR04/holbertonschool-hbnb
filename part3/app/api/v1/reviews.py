from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

# Create a namespace for reviews - groups all review-related endpoints
api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed'),
    'user_id': fields.String(required=True, description='ID of the user writing the review')
})

# Define a model for review updates (partial updates)
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating (1-5)')
})

# Define a model for review output (response)
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
    """
    Resource for managing the list of reviews.
    Handles GET (list all) and POST (create) operations.
    """
    
    @api.doc('list_reviews')
    @api.marshal_list_with(review_output_model)
    def get(self):
        """
        Retrieve all reviews.
        
        Returns:
            List of all reviews
        """
        reviews = facade.get_all_reviews()
        return reviews, 200

    @api.expect(review_model, validate=True)
    @api.marshal_with(review_output_model, code=201)
    def post(self):
        """
        Create a new review.
        
        Validates that both the place and user exist before creating.
        
        Returns:
            The newly created review object with 201 status code
        """
        review_data = api.payload
        
        # Verify the place exists
        place = facade.get_place(review_data['place_id'])
        if not place:
            api.abort(400, f"Place with ID {review_data['place_id']} not found")
        
        # Verify the user exists
        user = facade.get_user(review_data['user_id'])
        if not user:
            api.abort(400, f"User with ID {review_data['user_id']} not found")
        
        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            api.abort(400, str(e))
        
        if not new_review:
            api.abort(400, 'Failed to create review')
        
        # Return 201 (Created) status code
        return new_review, 201


@api.route('/<string:review_id>')
class ReviewDetail(Resource):
    """
    Resource for managing individual review details.
    Handles GET (retrieve) and PUT (update) operations.
    """
    
    @api.doc('get_review')
    @api.marshal_with(review_output_model)
    def get(self, review_id):
        """
        Retrieve a review by ID.
        
        Args:
            review_id: The ID of the review to retrieve
        
        Returns:
            Review object or 404 error if not found
        """
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Review {review_id} not found")
        
        return review, 200

    @api.expect(review_update_model, validate=True)
    @api.marshal_with(review_output_model)
    def put(self, review_id):
        """
        Update a review's information.
        
        Args:
            review_id: The ID of the review to update
            
        Returns:
            Updated review object or 404 error if not found
        """
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Review {review_id} not found")
        
        review_data = api.payload
        
        # Update the review through the facade
        try:
            updated_review = facade.update_review(review_id, review_data)
        except ValueError as e:
            api.abort(400, str(e))
        
        if not updated_review:
            api.abort(400, 'Failed to update review')
        
        return updated_review, 200

    @api.doc('delete_review')
    def delete(self, review_id):
        """
        Delete a review.
        
        Args:
            review_id: The ID of the review to delete
        
        Returns:
            Empty response with 204 status code on success, or 404 error if not found
        """
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, f"Review {review_id} not found")
        
        # Delete the review through the facade
        success = facade.delete_review(review_id)
        
        if not success:
            api.abort(400, 'Failed to delete review')
        
        return '', 204


@api.route('/places/<string:place_id>')
class PlaceReviews(Resource):
    """
    Resource for retrieving all reviews for a specific place.
    """
    
    @api.doc('get_place_reviews')
    @api.marshal_list_with(review_output_model)
    def get(self, place_id):
        """
        Retrieve all reviews for a specific place.
        
        Args:
            place_id: The ID of the place
        
        Returns:
            List of reviews for that place
        """
        # Verify the place exists
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place {place_id} not found")
        
        reviews = facade.get_reviews_by_place(place_id)
        return reviews, 200
