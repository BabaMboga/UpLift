from flask import Flask, request, jsonify, make_response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity ,verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Charity, Donation, Beneficiary, Inventory , CharityApplication
import os
from sqlalchemy.orm import Session
import paypalrestsdk
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
  
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uplift.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-jwt-secret-key'  # Change this to a strong secret key
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


jwt = JWTManager(app)

CORS(app)

migrate = Migrate(app,db)
db.init_app(app)



@app.route('/', endpoint="index")
def index():
    return "This is The UpLift User/Charit/Donation/Beneficiary/Inventory API"

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json

    # Extract signup data from request
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    # Create a new user instance
    new_user = User(email=email, password=password, role=role)

    try:
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User signed up successfully.'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An error occurred while signing up.'}), 500

@app.route('/login', endpoint="login", methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    print("User:", user)
    
    if user and user.password == password:
        if user.role == 'donor' or user.role == 'charity' or user.role == 'admin':
            access_token = create_access_token(identity=user.id)  # Assuming your user ID field is named 'id'
            print("Access Token:", access_token)  # Debug print the access token
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

# Add this decorator to verify JWT in the request before accessing the identity
@app.before_request
def before_request():
    verify_jwt_in_request(optional=True)
    
@app.route('/protected', methods=['GET'])
@jwt_required()  # This decorator ensures that a valid JWT is required for access
def protected_route():
    user_id = get_jwt_identity()
    # Now you can use the user_id to retrieve user-specific information
    return jsonify({'message': 'You have access to this protected route.', 'user_id': user_id})


#sendgrid routes
@app.route('/send-reminder-email', methods=['POST'])
def send_reminder_email():
    data = request.json
    email = data.get('email')
    subject = "Monthly Donation Reminder"
    body = "This is a friendly reminder to make your monthly donation. Thank you for your support!"

    try:
        message = Mail(
            from_email='your_email@example.com',  # Set your SendGrid verified email address
            to_emails=email,
            subject=subject,
            plain_text_content=body
        )
        sg = SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        return jsonify({'message': 'Reminder email sent successfully.'}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to send reminder email.', 'details': str(e)}), 500



@app.route('/admin/beneficiaries',endpoint="get_beneficiaries", methods=['GET'])
# @jwt_required
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
    
    
    
    
    
# Replace with your PayPal Sandbox credentials
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "AcSW62OCv_utXTB8CGIoaQWulKSEgrYFUYX9_gkud-MODoW4lfx-9WiPb6QlmJIw3k8JQH8fiH62tx7O",
    "client_secret": "EAjmdD2daF8pxiQ3dh3iSOsDmtv-RuifD-TyV_NcivBMOMmKmeESlLY_VNea-mzR2MF_Q1CitYyvgiuP"
})

@app.route('/create-paypal-order', methods=['POST'])
def create_paypal_order():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "YOUR_RETURN_URL",
            "cancel_url": "YOUR_CANCEL_URL"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Sample Item",
                    "sku": "item",
                    "price": "10.00",
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": "10.00",
                "currency": "USD"
            },
            "description": "Sample Description"
        }]
    })

    if payment.create():
        approval_url = next(link.href for link in payment.links if link.rel == 'approval_url')
        return jsonify({'approval_url': approval_url})
    else:
        return jsonify({'error': payment.error})




    
    
    
if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    

    
