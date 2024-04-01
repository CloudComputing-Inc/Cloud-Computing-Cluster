from flask import Flask, request, jsonify
from api.metadata_routes import metadata_bp

app = Flask(__name__)
app.register_blueprint(metadata_bp)

@app.route('/')
def default_route():
    return "Welcome to the Market Performance API!"

if __name__ == '__main__':
    app.run(debug=True)