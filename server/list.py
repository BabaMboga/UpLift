from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///donations_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Charity(db.Model):
    # ... (existing Charity model)

class Beneficiary(db.Model):
    __tablename__ = 'beneficiaries'

    beneficiary_id = db.Column(db.Integer, primary_key=True)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.charity_id'), nullable=False)
    beneficiary_name = db.Column(db.String(100), nullable=False)
    story = db.Column(db.Text)

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

if __name__ == '__main__':
    app.run()
