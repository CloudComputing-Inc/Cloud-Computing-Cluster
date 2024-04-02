import connexion
from flask_cors import CORS
from flask import jsonify

# Create the application instance
app = connexion.App(__name__, specification_dir="./")

# read the swagger.yml file to configure the endpoints
app.add_api("swagger.yml")

# Enable CORS
CORS(app.app)

# Define a route for the root URL
@app.app.route('/')
def welcome():
    response = {
        "Welcome": "Welcome to the Amazon Reviews Analyzer API!",
        "Note": "Please refer to the Swagger UI for more detailed information on each endpoint.",
        "Endpoints": {
            "/api/v1/categories": "Retrieve a list of product categories.",
            "/api/v1/metadata": "Fetch metadata for products with optional filtering.",
            "/api/v1/top-brand": "Get the top brand in a specified category.",
            "/api/v1/top-products": "Retrieve top products in a category."
        }
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
