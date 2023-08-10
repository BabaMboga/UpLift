![My Image](/resources/logo.png)

# UpLift: Elevate Lives Illuminate Dreams

#### This MVP showcases an automated donation platform that serves an admin, a charity and a donor for a pleasing user experience while donating or viewing a charity of their choice.(version 3.10.08.2023), 08/10/2023


#### By **Ayim William, Ronald Luvega, Kennedy Kawawa, Collins Kimani, Joshua Chebulobi & Melvin James**

## Description
Uplift is a dynamic and user-centric platform that brings together individuals, charities and donors to create a positive impact on society. Our platform provides a seamless way for users to contribute to causes they care about, whether it's supporting local charities, making donations, or assisting beneficiaries in need.


### Key Features

#### User-Friendly Interface: 
Our platform offers an intuitive and easy-to-navigate interface that allows users to quickly find and engage with charitable organizations and initiatives.

#### Diverse Roles: 
UpLift caters to different user roles, including regular donors, charities, and administrators. Each role has access to specific functionalities tailored to their needs.

#### Secure Authentication:
We ensure the security of user data with robust authentication mechanisms. User information is protected, and access to sensitive features is controlled through secure JWT tokens.

#### Charity Approval and Management: 
Charities can apply to join our platform, and administrators can review and approve new charity applications. Approved charities can manage their profiles, share their mission, and provide updates on their initiatives.

#### Donations and Impact Tracking: 
Users can make donations to their chosen charities directly through our platform. Donors receive real-time updates on how their contributions are making a difference in the community.

#### Beneficiary Support: 
Charities can list beneficiaries and share their stories. Users can explore and learn about individuals in need and extend support through donations.

#### Inventory Management: 
Charities can manage their inventory of donated items and keep track of what they receive and distribute.

#### Transparent Reporting: 
We believe in transparency. Charities can provide detailed reports on how the funds they receive are being used, fostering trust between donors and organizations.

## Demo

![My Image](/resources/Screenshot-2023-08-10-1.png)

![My Image](/resources/Screenshot-2023-08-10-2.png)

![My Image](/resources/Screenshot-2023-08-10-3.png)

Use the link provided to navigate to UpLift ("")

## Setup/Installation Requirements

1. Clone the repository: 'git clone https://github.com/BabaMboga/UpLift.git'
2. cd into the client directory and run 'npm install --legacy-peer-deps' to install frontend dependencies
3. then run npm start 
4. cd into the server directory and run 'pipenv install && pipenv shell' to install backend dependencies
5. Run the following three codes in order:  
        - export FLASK_APP=app.py
        - export FLASK_RUN_PORT=5555
        - flask run

## Technologies Used

### Backend Technologies:

Flask: A micro web framework for Python used for building the backend of the application.
Flask-SQLAlchemy: An extension for Flask that simplifies working with relational databases using SQLAlchemy.
SQLAlchemy: An SQL toolkit and Object-Relational Mapping (ORM) library for Python.
email-validator: A library for validating email addresses.
Flask-Migrate: An extension for Flask that handles database migrations.
Python: The programming language used for backend development.

### Frontend Technologies:

React: A JavaScript library for building user interfaces.
Tailwind CSS: A utility-first CSS framework for quickly styling user interfaces.
JavaScript: The programming language used for frontend development.
HTML: The markup language used for structuring the frontend content.
CSS: Cascading Style Sheets used for styling the frontend.

### Database:

SQLite : 

### Additional Libraries:

sqlalchemy_serializer: A library that provides serialization capabilities for SQLAlchemy models.
Flask extensions: While not explicitly mentioned in the code snippets, various Flask extensions might be used for features like authentication, API handling, and more.

### Git: Version control system for tracking changes in the codebase.

To ensure code evolution was well documented from start to finish and made it easier to debug and fix any errors.

## Contact US
We welcome contributions from the community! Whether it's reporting issues, submitting feature requests, or creating pull requests, your input helps us make UpLift better for everyone.

For any issues, questions, suggestions or contributions please email any of us on any of the below addresses:

odhisayim@gmail.com
luvegaronny@gmail.com
kimanicollin@gmail.com

## License

UpLift is licensed under the Apache 2.0 License. See `LICENSE` for more information.
 
Join us in empowering positive change with UpLift!