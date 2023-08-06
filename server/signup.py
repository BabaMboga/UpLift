from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations.db'
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'  # Change this to a strong secret key
jwt = JWTManager(app)

# Manually create the application context
# with app.app_context():
    # Create the database tables (Since we removed User table, we don't need this anymore)
    # db.create_all()

@app.route('/signup', methods=['POST'])@jwt_required  # Require a valid JWT token to access this endpoint
def signup():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing JSON data in the request'}), 400

    role = data.get('role')
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    if not role or not username or not first_name or not last_name or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    if role not in ('user', 'admin', 'charity'):
        return jsonify({'message': 'Invalid role'}), 400

    # Save the user information in the database (code to save data to the database goes here)

    return jsonify({'message': 'User created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
