from flask_restx import Namespace, Resource, fields
from app.services.facade import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

# Model for updates (all fields optional)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    def get(self):
        """Retrieve a list of all users"""
        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        } for user in users], 200

    @api.expect(user_model, validate=True)
    @api.doc('create_user')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        
        # Check if email already exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email,
            'created_at': new_user.created_at.isoformat(),
            'updated_at': new_user.updated_at.isoformat()
        }, 201

@api.route('/<user_id>')
class UserResource(Resource):
    @api.doc('get_user')
    def get(self, user_id):
        """Retrieve a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat()
        }, 200

    @api.expect(user_update_model, validate=True)
    @api.doc('update_user')
    def put(self, user_id):
        """Update a user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        user_data = api.payload
        
        # Check if email is being changed and if new email already exists
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400
        
        updated_user = facade.update_user(user_id, user_data)
        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'created_at': updated_user.created_at.isoformat(),
            'updated_at': updated_user.updated_at.isoformat()
        }, 200
