from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# class Charity(db.Model):
    # ... (existing Charity model)

class Beneficiary(db.Model):
    beneficiary_id = db.Column(db.Integer, primary_key=True)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.charity_id'), nullable=False)
    beneficiary_name = db.Column(db.String, nullable=False)
    story = db.Column(db.String)

class Inventory(db.Model):
    inventory_id = db.Column(db.Integer, primary_key=True)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.charity_id'), nullable=False)
    item_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/admin/beneficiaries', methods=['GET'])
def get_beneficiaries_for_admin():
    beneficiaries_list = []

    for beneficiary in Beneficiary.query.all():
        beneficiaries_list.append({
            'beneficiary_id': beneficiary.beneficiary_id,
            'charity_id': beneficiary.charity_id,
            'beneficiary_name': beneficiary.beneficiary_name,
            'story': beneficiary.story
        })

    return jsonify({'beneficiaries': beneficiaries_list}), 200

@app.route('/admin/inventory', methods=['GET'])
def get_inventory_for_admin():
    inventory_list = []

    for inventory_item in Inventory.query.all():
        inventory_list.append({
            'inventory_id': inventory_item.inventory_id,
            'charity_id': inventory_item.charity_id,
            'item_name': inventory_item.item_name,
            'quantity': inventory_item.quantity,
            'date_sent': inventory_item.date_sent
        })

    return jsonify({'inventory': inventory_list}), 200

if __name__ == '__main__':
    app.run(debug=True)
