from flask import Flask, render_template, request, redirect, url_for
import stripe

app = Flask(__name__)

public_key = "pk_test_51NadRLFqVq6HkR6T1QVIl6S35zDZ0F91YxHGxybrzGMAezcaRHUtPIPYBixjguzql5Xdn08CdNB0KAAmRqFNYrpE00LjD70O6S"
stripe.api_key = "sk_test_51NadRLFqVq6HkR6Txnzx9c98JRjpoIp4AoJjXgKFNNr9Zqz6jA2Ampx1veT5vdYde5wteD8e8WZaQyf9jexgeShV00FfUY3mAq"


@app.route('/')
def index():
    return render_template('index.html', public_key=public_key)


@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')


@app.route('/payment', methods=['POST'])
def payment():
    # customer
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1999,
        currency='usd',
        description='donations'
    )

    return redirect(url_for('thankyou'))


if __name__ == '__main__':
    app.run()
