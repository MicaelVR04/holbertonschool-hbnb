from flask import Flask
from app.api import blueprint
from config import config

app = Flask(__name__)
app.config.from_object(config['default'])

# Register the API blueprint
app.register_blueprint(blueprint)

@app.route('/')
def hello():
    return "HBnB Project is Running!"

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
