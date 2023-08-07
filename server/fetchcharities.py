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

@app.route('/charities', methods=['GET'])
def get_charities():
    charities = Charity.query.filter_by(status=True).all()

    if not charities:
        return jsonify({'message': 'No active charities found.'}), 404

    charity_list = [{'charity_id': charity.charity_id, 'name': charity.name} for charity in charities]
    return jsonify({'charities': charity_list}), 200

if __name__ == '__main__':
    app.run()
