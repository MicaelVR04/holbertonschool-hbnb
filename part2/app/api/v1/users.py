from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

# Create a namespace for users - groups all user-related endpoints
api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
# This tells Flask-RESTx what fields are required for user creation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

# Define a model for user updates (all fields optional for partial updates)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

# Define a model for user output (response)
user_output_model = api.model('UserOutput', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})


@api.route('/')
class UserList(Resource):
    """
    Resource for managing the list of users.
    Handles GET (list all) and POST (create) operations.
    """
    
    @api.doc('list_users')
    @api.marshal_list_with(user_output_model)
    def get(self):
        """
        Retrieve all users.
        
        Returns:
            List of all users (without passwords)
        """
        users = facade.get_all_users()
        return users, 200

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_output_model, code=201)
    def post(self):
        """
        Register a new user.
        
        Validates that email isn't already in use, then creates new user.
        
        Returns:
            The newly created user object with 201 status code
        """
        user_data = api.payload
        
        # Check if email already exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            api.abort(400, 'Email already registered')

        # Create the user through the facade
        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            api.abort(400, str(e))
        
        # Return 201 (Created) status code
        return new_user, 201


@api.route('/<string:user_id>')
class UserDetail(Resource):
    """
    Resource for managing individual user details.
    Handles GET (retrieve) and PUT (update) operations.
    """
    
    @api.doc('get_user')
    @api.marshal_with(user_output_model)
    def get(self, user_id):
        """
        Retrieve a user by ID.
        
        Args:
            user_id: The ID of the user to retrieve
        
        Returns:
            User object or 404 error if not found
        """
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")
        
        return user, 200

    @api.expect(user_update_model, validate=True)
    @api.marshal_with(user_output_model)
    def put(self, user_id):
        """
        Update a user's information.
        
        Args:
            user_id: The ID of the user to update
            
        Returns:
            Updated user object or 404 error if not found
        """
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")
        
        user_data = api.payload
        
        # Check if email is being changed to an existing one
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                api.abort(400, 'Email already registered')
        
        # Update the user through the facade
        try:
            updated_user = facade.update_user(user_id, user_data)
        except ValueError as e:
            api.abort(400, str(e))
        
        return updated_user, 200
