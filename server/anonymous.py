from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/donate', methods=['POST'])
def donate():
    data = request.json
    amount = data.get('amount')
    is_recurring = data.get('isRecurring')
    start_date = data.get('startDate')
    end_date = data.get('endDate')

    # Process the donation data and store it in your database
    # You can also send confirmation emails, update charity data, etc.

    return jsonify({'message': 'Donation successful!'})

if __name__ == '__main__':
    app.run(debug=True)
