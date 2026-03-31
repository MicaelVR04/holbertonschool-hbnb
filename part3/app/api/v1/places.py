from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(description='ID of the owner (ignored, taken from token)')
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate')
})


def serialize_review(review):
    return {
        "id": review.id,
        "text": review.text,
        "rating": review.rating,
        "user_id": review.user_id,
        "place_id": review.place_id,
        "created_at": str(review.created_at),
        "updated_at": str(review.updated_at)
    }


def serialize_amenity(amenity):
    return {
        "id": amenity.id,
        "name": amenity.name
    }


def serialize_place(place):
    amenities = []
    if getattr(place, "amenities", None):
        amenities = [serialize_amenity(amenity) for amenity in place.amenities]

    reviews = []
    if getattr(place, "reviews", None):
        reviews = [serialize_review(review) for review in place.reviews]

    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner_id": place.owner_id,
        "reviews": reviews,
        "amenities": amenities,
        "created_at": str(place.created_at),
        "updated_at": str(place.updated_at)
    }


@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    def get(self):
        places = facade.get_all_places()
        return [serialize_place(place) for place in places], 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    def post(self):
        place_data = api.payload
        current_user = get_jwt_identity()
        place_data['owner_id'] = current_user

        new_place = facade.create_place(place_data)
        if not new_place:
            api.abort(400, 'Failed to create place')

        return serialize_place(new_place), 201


@api.route('/<string:place_id>')
class PlaceDetail(Resource):
    @api.doc('get_place')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place {place_id} not found")
        return serialize_place(place), 200

    @jwt_required()
    @api.expect(place_update_model, validate=True)
    def put(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place {place_id} not found")

        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        current_user = get_jwt_identity()

        place_owner_id = getattr(place, 'owner_id', None)
        if not place_owner_id and getattr(place, 'owner', None):
            place_owner_id = getattr(place.owner, 'id', None)

        if not is_admin and place_owner_id != current_user:
            api.abort(403, "Unauthorized action")

        updated_place = facade.update_place(place_id, api.payload)
        if not updated_place:
            api.abort(400, 'Failed to update place')

        return serialize_place(updated_place), 200
