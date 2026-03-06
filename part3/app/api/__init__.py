from flask_restx import Api
from flask import Blueprint
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

# Create a blueprint for the API
blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

# Create the Api object
api = Api(blueprint,
    title='HBnB API',
    version='1.0',
    description='The HBnB Application API'
)

# Register all namespaces (endpoint groups)
api.add_namespace(users_ns, path='/users')
api.add_namespace(amenities_ns, path='/amenities')
api.add_namespace(places_ns, path='/places')
api.add_namespace(reviews_ns, path='/reviews')
