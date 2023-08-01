from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Charity, Donation, Beneficiary, Inventory
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uplift.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'  # Change this to a strong secret key
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


jwt = JWTManager(app)
#allows all origins and should be changed after development
CORS(app, resources={r"/*": {"origins":"*"}})
#when in production
#CORS(app, resources={r"/*": {"origins": "https://your_trusted-frontend-domain.com"}})
migrate = Migrate(app,db)
db.init_app(app)

# Manually create the application context
# with app.app_context():
    # Create the database tables (Since we removed User table, we don't need this anymore)
    # db.create_all()

@app.route('/')
def index():
    return "This is The UpLift User/Charit/Donation/Beneficiary/Inventory API"

@app.route('/signup', methods=['POST'])  # Require a valid JWT token to access this endpoint
def signup():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing JSON data in the request'}), 400

    # Extract data from the JSON request
    role = data.get('role')
    username = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    #Validate required fields
    if not role or not username or not first_name or not last_name or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    #Validate role
    if role not in ('user', 'admin', 'charity'):
        return jsonify({'message': 'Invalid role'}), 400
    
    #Validate email format
    if '@' not in email or '.' not in email:
        return jsonify({'message':'Invalid email format'}), 400
    
    #Check if the email is already registered
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email is already registered'}), 400
    
    #Generate a password hash
    hashed_password = generate_password_hash(password)

    #Create a new User object
    new_user = User(
        email=email,
        password=hashed_password,
        role=role,
        user_name=username,
        first_name=first_name,
        second_name=last_name
    )

    # Save the user information in the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing JSON data in the request'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    # Retrieve the user from the database
    user = User.query.filter_by(user_name=username).first()

    #Check if the user exists and validate the password
    if not user or not check_password_hash(user.password,password):
        return jsonify({'message':'Invalid username or password'}), 401

    # Generate an access token for the authenticated user
    access_token = create_access_token(identity=user.id)

    return jsonify({'access_token': access_token}), 200

if __name__ == '__main__':
    app.run(debug=True)
