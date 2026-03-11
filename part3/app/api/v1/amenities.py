from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services.facade import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_output_model = api.model('AmenityOutput', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_output_model)
    def get(self):
        amenities = facade.get_all_amenities()
        return amenities, 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_output_model, code=201)
    def post(self):
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, "Admin privileges required")

        amenity_data = api.payload
        new_amenity = facade.create_amenity(amenity_data)
        return new_amenity, 201


@api.route('/<string:amenity_id>')
class AmenityDetail(Resource):
    @api.doc('get_amenity')
    @api.marshal_with(amenity_output_model)
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity {amenity_id} not found")
        return amenity, 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_output_model)
    def put(self, amenity_id):
        claims = get_jwt()
        if not claims.get('is_admin', False):
            api.abort(403, "Admin privileges required")

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity {amenity_id} not found")

        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        return updated_amenity, 200
