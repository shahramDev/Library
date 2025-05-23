from flask import Flask, request, jsonify
import json
import os

API_KEY = "HERE_IS_THE_API_KEY"
DATABASE_PATH = "database/payments.json"

app = Flask(__name__)

@app.route('/', methods=['POST'])
def update_payment_status():
    if request.method == 'POST':
        if request.form and 'API_KEY' in request.form and 'price' in request.form and request.form['API_KEY'] == API_KEY:
            price = request.form['price']
            if os.path.exists(DATABASE_PATH):
                with open(DATABASE_PATH, 'r') as file:
                    payments = json.load(file)

                if price in payments:
                    payments[price]['status'] = True
                    with open(DATABASE_PATH, 'w') as file:
                        json.dump(payments, file, indent=4)

    return '', 204  # No content

if __name__ == '__main__':
    app.run()
