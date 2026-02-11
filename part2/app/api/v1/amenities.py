from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

# Create a namespace for amenities - groups all amenity-related endpoints
api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

# Define a model for amenity output (response)
amenity_output_model = api.model('AmenityOutput', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class AmenityList(Resource):
    """
    Resource for managing the list of amenities.
    Handles GET (list all) and POST (create) operations.
    """
    
    @api.doc('list_amenities')
    @api.marshal_list_with(amenity_output_model)
    def get(self):
        """
        Retrieve all amenities.
        
        Returns:
            List of all amenities
        """
        amenities = facade.get_all_amenities()
        return amenities, 200

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_output_model, code=201)
    def post(self):
        """
        Create a new amenity.
        
        Returns:
            The newly created amenity object with 201 status code
        """
        amenity_data = api.payload
        
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            api.abort(400, str(e))
        
        # Return 201 (Created) status code
        return new_amenity, 201


@api.route('/<string:amenity_id>')
class AmenityDetail(Resource):
    """
    Resource for managing individual amenity details.
    Handles GET (retrieve) and PUT (update) operations.
    """
    
    @api.doc('get_amenity')
    @api.marshal_with(amenity_output_model)
    def get(self, amenity_id):
        """
        Retrieve an amenity by ID.
        
        Args:
            amenity_id: The ID of the amenity to retrieve
        
        Returns:
            Amenity object or 404 error if not found
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity {amenity_id} not found")
        
        return amenity, 200

    @api.expect(amenity_model, validate=True)
    @api.marshal_with(amenity_output_model)
    def put(self, amenity_id):
        """
        Update an amenity's information.
        
        Args:
            amenity_id: The ID of the amenity to update
            
        Returns:
            Updated amenity object or 404 error if not found
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity {amenity_id} not found")
        
        amenity_data = api.payload
        
        # Update the amenity through the facade
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            api.abort(400, str(e))
        
        return updated_amenity, 200
