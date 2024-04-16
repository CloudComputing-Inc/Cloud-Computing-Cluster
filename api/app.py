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
            "/api/v1/categories": "Retrieve a list of product categories. No additional fields required.",
            "/api/v1/metadata?category={category}&brand={brand}&minPrice={minPrice}&maxPrice={maxPrice}": "Fetch metadata for products with optional filtering. Replace {category} with the product category (required), {brand} with the product brand (optional), {minPrice} with the minimum price (optional), {maxPrice} with the maximum price (optional).",
            "/api/v1/top-brand?category={category}": "Get the top brand in a specified category. Replace {category} with the product category (required).",
            "/api/v1/top-products?category={category}": "Retrieve top products in a category. Replace {category} with the product category (required)."
        }
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
