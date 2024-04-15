from flask import Flask, jsonify
from authlib.integrations.flask_oauth2 import ResourceProtector
from validator import Auth0JWTBearerTokenValidator

# Create the Flask app
app = Flask(__name__)

# Create a ResourceProtector instance
require_auth = ResourceProtector()

# Initialize the JWT token validator with Auth0 domain and audience
validator = Auth0JWTBearerTokenValidator(
    "your-auth0-domain.com",
    "your-api-identifier"
)

# Register the token validator with the resource protector
require_auth.register_token_validator(validator)

# Define public endpoint (no authentication required)
@app.route("/api/public")
def public():
    response = "This is a public endpoint. No authentication required."
    return jsonify(message=response)

# Define private endpoint (requires authentication)
@app.route("/api/private")
@require_auth(None)  # No specific scope required, just authentication
def private():
    response = "This is a private endpoint. Authentication required."
    return jsonify(message=response)

# Define private scoped endpoint (requires specific scope)
@app.route("/api/private-scoped")
@require_auth("read:messages")  # Requires 'read:messages' scope
def private_scoped():
    response = "This is a private scoped endpoint. Authentication and 'read:messages' scope required."
    return jsonify(message=response)

if __name__ == "__main__":
    app.run(debug=True)
