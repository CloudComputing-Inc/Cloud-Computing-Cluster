from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

@app.route('/categories', methods=['GET'])
def get_categories():
    params = {
        'locale': request.args.get('locale', 'en_US')  # Default to 'en_US' if no locale is provided
    }
    headers = {
        'Authorization': 'Bearer YOUR_YELP_API_KEY'
    }
    response = requests.get('https://api.yelp.com/v3/categories', headers=headers, params=params)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
