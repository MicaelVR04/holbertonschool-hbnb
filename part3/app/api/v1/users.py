from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.facade import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(description='Admin flag')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password of the user'),
    'is_admin': fields.Boolean(description='Admin flag')
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

    @jwt_required(optional=True)
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_created_model, code=201)
    def post(self):
        """
        Bootstrap rule:
        - If there are no users yet, allow creation without token (to create first admin).
        - After first user exists, only admins can create users.
        """
        users = facade.get_all_users()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False) if claims else False

        if len(users) > 0 and not is_admin:
            api.abort(403, "Admin privileges required")

        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            api.abort(400, 'Email already registered')

        new_user = facade.create_user(user_data)
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
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        current_user = get_jwt_identity()

        user = facade.get_user(user_id)
        if not user:
            api.abort(404, f"User {user_id} not found")

        user_data = api.payload

        if not is_admin:
            if user_id != current_user:
                api.abort(403, "Unauthorized action")
            if 'email' in user_data or 'password' in user_data or 'is_admin' in user_data:
                api.abort(400, "You cannot modify email or password.")

        if 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                api.abort(400, "Email already registered")

        if 'password' in user_data:
            user.hash_password(user_data['password'])
            user_data.pop('password')

        if 'is_admin' in user_data and is_admin:
            user_data['is_admin'] = bool(user_data['is_admin'])

        updated_user = facade.update_user(user_id, user_data)
        return updated_user, 200
