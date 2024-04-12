import flask
from flask import request, jsonify

app = flask.Flask(__name__)

@app.route('/recommendations', methods=['GET'])
def recommendations():
    return jsonify({
        'recommendations': [
            'The Shawshank Redemption',
            'The Godfather',
            'The Dark Knight',
            'The Lord of the Rings: The Return of the King',
            'Pulp Fiction'
        ]
    })

if __name__ == '__main__':
    app.run(port=5001)

    