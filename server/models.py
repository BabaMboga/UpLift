from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func


db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique = True)
    password = db.Column(db.String, nullable = False, )
    role = db.Column(db.String, nullable=False)
    user_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    second_name = db.Column(db.String, nullable=False)

    donations = db.relationship('Donation', backref='donor')

    serialize_rules = ("-donation.user")

    def __repr__(self):
        return f'User: {self.user_name}, ID: {self.id}, Role: {self.role}'

class Charity(db.Model, SerializerMixin):
    __tablename__ = 'charities'

    charity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    amount_received = db.Column(db.Integer)

    beneficiaries = db.relationship('Beneficiary', backref='charity')
    donations = db.relationship('Donation', backref='charity')
    inventory = db.relationship('Inventory', backref='charity')

    serialize_rules = ("-beneficiaries.charity", "-donations.charity", "-inventory.charity")

    def __repr__(self):
        return f'Name: {self.name} of ID: {self.charity_id} has received {self.amount_received}'

class Donation(db.Model, SerializerMixin):
    __tablename__ = 'donations'

    donation_id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.charity_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    donation_date = db.Column(db.DateTime, default=func.now())
    is_anonymous = db.Column(db.Boolean, nullable=False)

    #Donation schedule fields
    schedule_start_date = db.Column(db.DateTime)
    schedule_end_date = db.Column(db.DateTime)
    schedule_frequency = db.Column(db.String)

    serialize_rules = ("-users.donations", "-charities.donations")


    def __repr__(self):
        return f"{self.amount} was donated on {self.donation_date} by donor of ID: {self.donor_id}"

class Beneficiary(db.Model, SerializerMixin):
    __tablename__ = 'beneficiaries'

    beneficiary_id = db.Column(db.Integer, primary_key=True)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.charity_id'), nullable=False)
    beneficiary_name = db.Column(db.String, nullable=False)
    story = db.Column(db.String)

    serialize_rules = ("-charity.beneficiaries")

    def __repr__(self):
        return f"{self.beneficiary_name} of charity ID:{self.charity_id} says {self.story}"
    

    

class Inventory(db.Model, SerializerMixin):
    __tablename__ = 'inventory'

    inventory_id = db.Column(db.Integer, primary_key=True)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.charity_id'), nullable=False)
    item_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_sent = db.Column(db.DateTime, nullable=False)

    serialize_rules = ("-charity.inventory")

    def __repr__(self):
        return f"{self.item_name} was sent on {self.date_sent} by charity{self.charity_id}"

    
