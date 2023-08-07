from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
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

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    # Retrieve the user from the database
    user = User.query.filter_by(email=email).first()

    #Check if the user exists and validate the password
    if not user or not check_password_hash(user.password,password):
        return jsonify({'message':'Invalid username or password'}), 401

    # Generate an access token for the authenticated user
    access_token = create_access_token(identity=user.id)

    return jsonify({'access_token': access_token}), 200

@app.route('/admins/<int:charity_id>', methods=['POST'])
@jwt_required #Return a valid JWT token to access this endpoint
def approve_delete_charity(charity_id):
    #Get the authenticated user's identity from the JWT token
    current_user_id = get_jwt_identity()

    #Retrieve the user from the database
    user = User.query.get(current_user_id)

    #Check if the user is an 'admin'
    if user.role != 'admin':
        return jsonify({'message': 'Unauthorized access'}), 403
    
    #Retrieve the charity from the database
    charity = Charity.query.get(charity_id)

    #Check if the charity exists
    if not charity:
        return jsonify({'message': 'Charity not found'}), 404
    
    #perform the actions based on the request data
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing JSON data in the request'}), 400
    
    action = data.get('action')

    if action =='approve':
        
        charity.status = True
        db.session.commit()
        return jsonify({'message': 'Charity approved successfully'}), 200
    elif action == 'delete':
        db.session.delete(charity)
        db.session.commit()
        return jsonify({'message': 'Charity deleted successfully'}), 200
    else:
        return jsonify({'message':'Invalid action'}), 400
    
@app.route('/beneficiaries', methods=['GET'])
@jwt_required
def get_all_beneficiaries():
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)

    if user.role not in ('admin', 'charity'):
        return make_response(
            jsonify({'message': 'Unauthorized access'}),
            403
        )
    
    beneficiaries = Beneficiary.query.all()

    beneficiaries_data = [beneficiary.to_dict() for beneficiary in beneficiaries]

    response = make_response(jsonify({'beneficiaries': beneficiaries_data}),
                             200
                )

    return response
@app.route('/charities', methods=['GET'])
@jwt_required
def get_charities():
    charities = Charity.query.filter_by(status=True).all()

    if not charities:
        return jsonify({'message': 'No active charities found.'}), 404

    charity_list = [{'charity_id': charity.charity_id, 'name': charity.name} for charity in charities]
    return jsonify({'charities': charity_list}), 200

@app.route('/charities', methods=['POST'])
def create_charity():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name or not description:
        return jsonify({'error': 'Both name and description are required.'}), 400

    new_charity = Charity(name=name, description=description, status=True, amount_received=0)
    db.session.add(new_charity)
    db.session.commit()

    return jsonify({'message': 'Charity created successfully.', 'charity_id': new_charity.charity_id}), 201

@app.route('/beneficiaies/<int:charity_id', methods=['GET'])
@jwt_required
def get_beneficiary_by_charity_id(charity_id):
    beneficiaries = Beneficiary.query.filter_by(charity_id=charity_id).all()
    

    if not beneficiaries:
        return jsonify({'message':'No beneficiaries for the selected charity found'}), 404
    
    beneficiaries_list = [beneficiary.to_dict() for beneficiary in beneficiaries]

    response = make_response(jsonify({'beneficiaries':beneficiaries_list}), 
                    200
                    )
    return response
    


if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
# @app.route('/charities', methods=['GET'])
# def get_charities():
#     charities = Charity.query.all()
#     data = {
#         "charities": [
#             {
#                 "id": charity.id,
#                 "name": charity.name,
#                 "logo": charity.logo,
#                 "total_amount_donated": charity.total_amount_donated,
#                 "testimonials": [
#                     {
#                         "author": testimonial.author,
#                         "testimonial": testimonial.testimonial
#                     }
#                     for testimonial in charity.testimonials
#                 ]
#             }
#             for charity in charities
#         ]
#     }
#     return jsonify(data)


# @app.route('/charities/<int:charity_id>', methods=['DELETE'])
# def delete_charity(charity_id):
#     try:
#         charity = Charity.query.get(charity_id)
#         if not charity:
#             return jsonify({"message": "Charity not found"}), 404

#         db.session.delete(charity)
#         db.session.commit()

#         return jsonify({"message": "Charity deleted successfully"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400




# @app.route('/application', methods=['POST'])
# def create_charity_application():
#     try:
#         data = request.get_json()
#         imageURL = data['imageURL']
#         name = data['name']
#         description = data['description']

#         application = CharityApplication(imageURL=imageURL, name=name, description=description)
#         db.session.add(application)
#         db.session.commit()

#         return jsonify({"message": "Charity application submitted successfully."}), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
    
    
# @app.route('/applications', methods=['GET'])
# def get_charity_applications():
#     try:
#         applications = CharityApplication.query.all()
#         application_list = [app.to_dict() for app in applications]
#         return jsonify(application_list), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400  
    
