from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    donations = relationship('Donation', back_populates='donor')

class Charity(Base):
    __tablename__ = 'charities'

    charity_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)
    amount_received = Column(Integer)

    beneficiaries = relationship('Beneficiary', back_populates='charity')
    donations = relationship('Donation', back_populates='charity')
    inventory_items = relationship('Inventory', back_populates='charity')

class Donation(Base):
    __tablename__ = 'donations'

    donation_id = Column(Integer, primary_key=True)
    donor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    charity_id = Column(Integer, ForeignKey('charities.charity_id'), nullable=False)
    amount = Column(Float, nullable=False)
    donation_date = Column(DateTime, nullable=False)
    is_anonymous = Column(Boolean, nullable=False)
    schedule_start_date = Column(DateTime)
    schedule_end_date = Column(DateTime)
    schedule_frequency = Column(String)

    donor = relationship('User', back_populates='donations')
    charity = relationship('Charity', back_populates='donations')

class Beneficiary(Base):
    __tablename__ = 'beneficiaries'

    beneficiary_id = Column(Integer, primary_key=True)
    charity_id = Column(Integer, ForeignKey('charities.charity_id'), nullable=False)
    beneficiary_name = Column(String, nullable=False)
    story = Column(String)

    charity = relationship('Charity', back_populates='beneficiaries')

class Inventory(Base):
    __tablename__ = 'inventory'

    inventory_id = Column(Integer, primary_key=True)
    charity_id = Column(Integer, ForeignKey('charities.charity_id'), nullable=False)
    item_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    date_sent = Column(DateTime, nullable=False)

    charity = relationship('Charity', back_populates='inventory_items')
