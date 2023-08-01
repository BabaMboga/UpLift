from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations.db'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing JSON data in the request'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    # Validate the user's credentials and retrieve the user from the database (code for validation and retrieval goes here)

    # For the sake of this example, we'll create a dummy access token
    access_token = 'dummy-access-token'

    return jsonify({'access_token': access_token}), 200

if __name__ == '__main__':
    app.run(debug=True)
