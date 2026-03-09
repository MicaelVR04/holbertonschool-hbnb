from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user')
})

user_output_model = api.model('UserOutput', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email'),
    'created_at': fields.String(description='Creation timestamp'),
    'updated_at': fields.String(description='Last update timestamp')
})

user_created_model = api.model('UserCreated', {
    'id': fields.String(description='User ID'),
    'message': fields.String(description='Success message')
})


@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.marshal_list_with(user_output_model)
    def get(self):
        users = facade.get_all_users()
        return users, 200

    @api.expect(user_model, validate=True)
    @api.marshal_with(user_created_model, code=201)
    def post(self):
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            api.abort(400, 'Email already registered')

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            api.abort(400, str(e))

        return {"id": new_user.id, "message": "User created successfully"}, 201


@api.route('/<string:user_id>')
class UserDetail(Resource):
    @api.doc('get_user')
    @api.marshal_with(user_output_model)
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")
        return user, 200

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.marshal_with(user_output_model)
    def put(self, user_id):
        current_user = get_jwt_identity()

        if user_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")

        user_data = api.payload

        if 'email' in user_data or 'password' in user_data:
            return {'error': 'You cannot modify email or password.'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
        except ValueError as e:
            api.abort(400, str(e))

        return updated_user, 200
