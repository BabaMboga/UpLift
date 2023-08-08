from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Charity, Donation, Beneficiary, Inventory , CharityApplication
import os
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uplift.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'  # Change this to a strong secret key
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


# jwt = JWTManager(app)

CORS(app)

migrate = Migrate(app,db)
db.init_app(app)



@app.route('/', endpoint="index")
def index():
    return "This is The UpLift User/Charit/Donation/Beneficiary/Inventory API"

@app.route('/signup',endpoint="signup", methods=['POST'])  # Require a valid JWT token to access this endpoint
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

@app.route('/login', endpoint="login", methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.password == password:
        if user.role == 'donor' or user.role == 'charity' or user.role == 'admin':
            access_token = create_access_token(identity=user.id)  # Assuming your user ID field is named 'id'
            return jsonify({
                'message': 'Login successful',
                'access_token': access_token,
                'user_id': user.id,
                'role': user.role
            })
        else:
            return jsonify({'message': 'Invalid user role'}), 403
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/admin/beneficiaries',endpoint="get_beneficiaries", methods=['GET'])
@jwt_required
def get_beneficiaries():
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
                             200)

    return response

@app.route('/charities', endpoint="get_charities", methods=['GET'])
# @jwt_required
def get_charities():
    charities = Charity.query.filter_by(status=True).all()

    if not charities:
        return jsonify({'message': 'No active charities found.'}), 404

    charity_list = [
        {
            'charity_id': charity.charity_id,
            'name': charity.name,
            'description': charity.description,
            'amount_received': charity.amount_received,
            'image_url': charity.image_url  # Include the image_url field
        }
        for charity in charities
    ]
    
    return jsonify({'charities': charity_list}), 200


@app.route('/api/charities/<int:charity_id>', methods=['DELETE'])
def delete_charity(charity_id):
    try:
        print("Deleting charity with ID:", charity_id)
        
        charity = Charity.query.filter_by(charity_id=charity_id).first()

        if not charity:
            print("Charity not found.")
            return jsonify({'message': 'Charity not found.'}), 404
        
        db.session.delete(charity)
        db.session.commit()
        
        print("Charity deleted successfully.")
        return jsonify({'message': 'Charity deleted successfully.'}), 200
    except Exception as e:
        db.session.rollback()
        print("Error:", e)
        return jsonify({'message': 'Failed to delete charity.', 'error': str(e)}), 500











@app.route('/beneficiaries/stories', endpoint="beneficiaries_stories", methods=['GET'])
# @jwt_required
def get_beneficiaries_stories():
    beneficiaries = Beneficiary.query.all()
    beneficiaries_list = [{
        'beneficiary_id': beneficiary.beneficiary_id,
        'charity_id': beneficiary.charity_id,
        'beneficiary_name': beneficiary.beneficiary_name,
        'story': beneficiary.story
    } for beneficiary in beneficiaries]

    return jsonify({'beneficiaries': beneficiaries_list}), 200

# API endpoint to get inventory for admin
@app.route('/admin/inventory', endpoint="inventory" ,methods=['GET'])
# @jwt_required
def get_inventory_for_admin():
    inventory_list = []
    for inventory_item in Inventory.query.all():
        inventory_list.append({
            'inventory_id': inventory_item.inventory_id,
            'charity_id': inventory_item.charity_id,
            'item_name': inventory_item.item_name,
            'quantity': inventory_item.quantity,
            'date_sent': inventory_item.date_sent.strftime('%Y-%m-%d %H:%M:%S')
        })

    return jsonify({'inventory': inventory_list}), 200



@app.route('/application', methods=['POST'])
def create_charity_application():
    try:
        data = request.get_json()
        imageURL = data['imageURL']
        name = data['name']
        description = data['description']

        application = CharityApplication(imageURL=imageURL, name=name, description=description)
        db.session.add(application)
        db.session.commit()

        return jsonify({"message": "Charity application submitted successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    
@app.route('/applications', methods=['GET'])
def get_charity_applications():
    try:
        applications = CharityApplication.query.all()
        application_list = [app.to_dict() for app in applications]
        return jsonify(application_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400   




    
    
    
if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    

    
