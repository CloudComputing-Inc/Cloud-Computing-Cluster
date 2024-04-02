""" 
from flask import Flask, request, jsonify
from api.metadata_routes import metadata_bp

app = Flask(__name__)
app.register_blueprint(metadata_bp)

@app.route('/')
def default_route():
    return "Welcome to the Market Performance API!"

if __name__ == '__main__':
    app.run(debug=True)
"""

# 3rd party modules
import connexion
from flask_cors import CORS

# Create the application instance
app = connexion.App(__name__, specification_dir="./")

# read the swagger.yml file to configure the endpoints
app.add_api("swagger.yml")
CORS(app.app)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
