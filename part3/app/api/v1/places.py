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

place_output_model = api.model('PlaceOutput', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title'),
    'description': fields.String(description='Description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'owner_id': fields.String(description='Owner (User) ID'),
    'reviews': fields.List(fields.String, description='List of review IDs'),
    'amenities': fields.List(fields.String, description='List of amenity IDs'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    @api.marshal_list_with(place_output_model)
    def get(self):
        places = facade.get_all_places()
        return places, 200

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.marshal_with(place_output_model, code=201)
    def post(self):
        place_data = api.payload
        current_user = get_jwt_identity()
        place_data['owner_id'] = current_user

        new_place = facade.create_place(place_data)
        if not new_place:
            api.abort(400, 'Failed to create place')

        return new_place, 201


@api.route('/<string:place_id>')
class PlaceDetail(Resource):
    @api.doc('get_place')
    @api.marshal_with(place_output_model)
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place {place_id} not found")
        return place, 200

    @jwt_required()
    @api.expect(place_update_model, validate=True)
    @api.marshal_with(place_output_model)
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

        return updated_place, 200
