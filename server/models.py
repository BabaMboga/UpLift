# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
# import os
# from app import db, User


# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uplift.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)
#     role = db.Column(db.String(20), nullable=False)
#     first_name = db.Column(db.String(80))
#     last_name = db.Column(db.String(80))

#     def __init__(self, email, username, password, role, first_name, last_name):
#         self.email = email
#         self.username = username
#         self.password = password
#         self.role = role
#         self.first_name = first_name
#         self.last_name = last_name

# with app.app_context():
#     db.create_all()

# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.get_json()
#     email = data.get('email')
#     username = data.get('username')
#     password = data.get('password')
#     role = data.get('role')
#     first_name = data.get('first_name')
#     last_name = data.get('last_name')

#     if not email or not username or not password or not role or not first_name or not last_name:
#         return jsonify({'message': 'Missing required fields'}), 400

#     if role not in ('user', 'admin', 'charity'):
#         return jsonify({'message': 'Invalid role'}), 400

#     if User.query.filter_by(username=username).first():
#         return jsonify({'message': 'Username already exists'}), 409

#     if User.query.filter_by(email=email).first():
#         return jsonify({'message': 'Email already exists'}), 409

#     hashed_password = generate_password_hash(password)
#     new_user = User(email=email, username=username, password=hashed_password, role=role, first_name=first_name, last_name=last_name)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User created successfully'}), 201


# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')

#     if not username or not password:
#         return jsonify({'message': 'Missing username or password'}), 400

#     user = User.query.filter_by(username=username).first()

#     if not user or not check_password_hash(user.password, password):
#         return jsonify({'message': 'Invalid username or password'}), 401

#     return jsonify({'message': 'Login successful'}), 200

# if __name__ == '__main__':
#     db.create_all()
#     app.run(debug=True)
    
#     # db.create_all()
#     # app.run(debug=True)

