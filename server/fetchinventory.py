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



if __name__ == '__main__':
    app.run(debug=True)
