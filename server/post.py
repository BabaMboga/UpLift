from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Charity(db.Model):
    __tablename__ = 'charities'

    charity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    amount_received = db.Column(db.Integer)

    beneficiaries = db.relationship('Beneficiary', backref='charity')
    donations = db.relationship('Donation', backref='charity')
    inventory = db.relationship('Inventory', backref='charity')

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

if __name__ == '__main__':
    app.run()
