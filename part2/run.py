from flask import Flask
from flask_restx import Api
from app.api.v1.users import api as users_ns

app = Flask(__name__)

# Create the Api instance and add namespaces
api = Api(app, version='1.0', title='HBnB API', description='A simple HBnB API')
api.add_namespace(users_ns, path='/api/v1/users')

@app.route('/')
def hello():
    return "HBnB Project is Running!"

if __name__ == '__main__':
    app.run(debug=True)
