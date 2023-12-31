from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.sql import func
from email_validator import validate_email, EmailNotValidError


db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    donations = db.relationship('Donation', backref='donor')

    serialize_rules = ("-donation.user")

    @db.validates('email')
    def validate_email(self, key, email):
        try:
            valid_email = validate_email(email)
            return valid_email.email
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email address: {e}")

    def __repr__(self):
        return f'User: ID: {self.id}, Role: {self.role}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'role': self.role
        }


class Charity(db.Model, SerializerMixin):
    __tablename__ = 'charities'

    charity_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    amount_received = db.Column(db.Integer)
    image_url = db.Column(db.String)  # Add the imageUrl attribute

    beneficiaries = db.relationship('Beneficiary', backref='charity', cascade='all, delete-orphan')
    donations = db.relationship('Donation', backref='charity', cascade='all, delete-orphan')
    inventory = db.relationship('Inventory', backref='charity', cascade='all, delete-orphan')

    serialize_rules = ("-beneficiaries.charity", "-donations.charity", "-inventory.charity")

    def __repr__(self):
        return f'Name: {self.name} of ID: {self.charity_id} has received {self.amount_received}'

    def to_dict(self):
        return {
            'charity_id': self.charity_id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'amount_received': self.amount_received,
            'image_url': self.image_url  # Include the imageUrl in the dictionary
        }


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
    
    def to_dict(self):
        return{
            'donation_id':self.donation_id,
            'donor_id': self.donor_id,
            'charity_id': self.charity_id,
            'amount':self.amount,
            'donation_date':self.donation_date,
            'is_anonymous': self.is_anonymous,
            'schedule_start_date': self.schedule_start_date,
            'schedule_end_date':self.schedule_end_date,
            'schedule_frequency':self.schedule_frequency
        }

class Beneficiary(db.Model, SerializerMixin):
    __tablename__ = 'beneficiaries'

    beneficiary_id = db.Column(db.Integer, primary_key=True)
    charity_id = db.Column(db.Integer, db.ForeignKey('charities.charity_id'), nullable=False)
    beneficiary_name = db.Column(db.String, nullable=False)
    story = db.Column(db.String)

    serialize_rules = ("-charity.beneficiaries")

    def __repr__(self):
        return f"{self.beneficiary_name} of charity ID:{self.charity_id} says {self.story}"
    
    def to_dict(self):
        return {
            'beneficiary_id': self.beneficiary_id,
            'charity_id': self.charity_id,
            'beneficiary_name': self.beneficiary_name,
            'story': self.story
        }

# Inventory Model
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
    
    def to_dict(self):
        return {
            'inventory_id': self.inventory_id,
            'charity_id': self.charity_id,
            'item_name': self.item_name,
            'quantity': self.quantity,
            'date_sent': self.date_sent.strftime('%Y-%m-%d %H:%M:%S')
        }
        
# class Charity(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     logo = db.Column(db.String(200), nullable=False)
#     total_amount_donated = db.Column(db.Float, default=0)
#     testimonials = db.relationship('Testimonial', backref='charity', lazy=True)

# class Testimonial(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     author = db.Column(db.String(100), nullable=False)
#     testimonial = db.Column(db.Text, nullable=False)
#     charity_id = db.Column(db.Integer, db.ForeignKey('charity.id'), nullable=False)
class CharityApplication(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    imageURL = db.Column(db.String(500), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "imageURL": self.imageURL,
            "name": self.name,
            "description": self.description,
        }    
      
      
        
