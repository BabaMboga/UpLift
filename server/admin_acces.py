from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Charity

app = Flask(__name__)

# Replace 'your_database_uri' with the actual URI for your database
engine = create_engine('')
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/approve_or_delete_charity/<int:charity_id>', methods=['POST'])
def approve_or_delete_charity(charity_id):
    """
    Endpoint to approve or delete a charity based on its ID.

    Parameters:
        charity_id (int): The ID of the charity to approve or delete.

    Returns:
        dict: A JSON response with a message indicating the status of the operation.
    """
    charity = session.query(Charity).filter_by(charity_id=charity_id).first()
    if charity is None:
        return jsonify({"message": "Charity not found."}), 404

    approve = request.json.get('approve', True)

    if approve:
        charity.status = True
        session.commit()
        return jsonify({"message": "Charity approved and visible to donors."}), 200
    else:
        session.delete(charity)
        session.commit()
        return jsonify({"message": "Charity deleted."}), 200

if __name__ == '__main__':
    app.run(debug=True)

