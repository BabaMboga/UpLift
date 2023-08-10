from flask import Flask, request
import requests
from requests.auth import HTTPBasicAuth
import json

app = Flask(__name__)


consumer_key = "czDU1qJDtkhfYapAosFZAezzt2wVrL1m"
consumer_secret = "ZJiMW22UALvlbEtu"
base_url = "https://sandbox.safaricom.co.ke"

@app.route('/stk_push')
def home():
    return 'Hello world'


@app.route('/access_token')
def token():
    data = ac_token()
    return data


@app.route('/register_urls')
def register():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % ac_token()}
    req_body = {
        "ShortCode": "600984",
        "ResponseType": "Completed",
        "ConfirmationURL": base_url + "/c2b/confirm",
        "ValidationURL": base_url + "/c2b/validation",
    }

    response_data = requests.post(
        mpesa_endpoint,
        json=req_body,
        headers=headers
    )

    return response_data.json()

@app.route('/c2b/confirm', methods=['POST'])
def confirm():
    # get data
    data = request.get_json
    # write to file
    file = open('confirm.json', 'a')
    file.write(json.dumps(data))
    file.close()
    return {
        "ReturnCode": 0,
        "ResultsDesc": "Accepted"
    }


@app.route('/c2b/validation', methods=['POST'])
def validate():
    # get data
    data = request.get_json
    # write to file
    file = open('confirm.json', 'a')
    file.write(json.dumps(data))
    file.close()
    return {
        "ReturnCode": 0,
        "ThirdPartyTransID": "Yay_my_sever",
        "ResultsDesc": "Accepted"
    }

# simulate
@app.route('/simulate')
def simulation():
    mpesa_endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
    access_token = ac_token()
    
    headers = {"Authorization": "Bearer %s" % access_token}
    request_body = {
        "ShortCode": "600984",
        "CommandID": "CustomerPayBillOnline",
        "BillRefNumber": "Testpay",
        "Msisdn": "254708374149",
        "Amount": 100
    }
    
    simulate_response = requests.post(mpesa_endpoint, json=request_body, headers=headers)
    return simulate_response.json()

def ac_token():
    mpesa_auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    data = requests.get(mpesa_auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret)).json()
    return data['access_token']

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3600, debug=True)
