from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

# Create a namespace for places - groups all place-related endpoints
api = Namespace('places', description='Place operations')

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='ID of the owner (User)')
})

# Define a model for place updates (partial updates)
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate')
})

# Define a model for place output (response)
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
    """
    Resource for managing the list of places.
    Handles GET (list all) and POST (create) operations.
    """
    
    @api.doc('list_places')
    @api.marshal_list_with(place_output_model)
    def get(self):
        """
        Retrieve all places.
        
        Returns:
            List of all places
        """
        places = facade.get_all_places()
        return places, 200

    @api.expect(place_model, validate=True)
    @api.marshal_with(place_output_model, code=201)
    def post(self):
        """
        Create a new place.
        
        Validates that the owner (user) exists before creating.
        
        Returns:
            The newly created place object with 201 status code
        """
        place_data = api.payload
        
        # Verify the owner exists
        owner = facade.get_user(place_data['owner_id'])
        if not owner:
            api.abort(400, f"Owner with ID {place_data['owner_id']} not found")
        
        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            api.abort(400, str(e))
        
        if not new_place:
            api.abort(400, 'Failed to create place')
        
        # Return 201 (Created) status code
        return new_place, 201


@api.route('/<string:place_id>')
class PlaceDetail(Resource):
    """
    Resource for managing individual place details.
    Handles GET (retrieve) and PUT (update) operations.
    """
    
    @api.doc('get_place')
    @api.marshal_with(place_output_model)
    def get(self, place_id):
        """
        Retrieve a place by ID.
        
        Args:
            place_id: The ID of the place to retrieve
        
        Returns:
            Place object or 404 error if not found
        """
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place {place_id} not found")
        
        return place, 200

    @api.expect(place_update_model, validate=True)
    @api.marshal_with(place_output_model)
    def put(self, place_id):
        """
        Update a place's information.
        
        Args:
            place_id: The ID of the place to update
            
        Returns:
            Updated place object or 404 error if not found
        """
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, f"Place {place_id} not found")
        
        place_data = api.payload
        
        # Update the place through the facade
        try:
            updated_place = facade.update_place(place_id, place_data)
        except ValueError as e:
            api.abort(400, str(e))
        
        if not updated_place:
            api.abort(400, 'Failed to update place')
        
        return updated_place, 200
