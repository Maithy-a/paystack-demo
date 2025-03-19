from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests
import logging
from datetime import datetime

# Load environment variables from .env
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')

# Configure logging
logging.basicConfig(
    filename='transactions.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/config')
def get_config():
    config = {
        "paystackPublicKey": os.getenv('PAYSTACK_PUBLIC_KEY')
    }
    print('Returning config:', config)  # Debug log
    return jsonify(config)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        data = request.get_json()
        print('Received payment data:', data)  # Debug log
        reference = data.get('reference')
        amount = data.get('amount')
        if not reference or not amount:
            print('Missing reference or amount')  # Debug log
            return jsonify({"status": "error", "message": "No reference or amount provided"}), 400

        # Verify transaction with Paystack
        url = "https://api.paystack.co/transaction/verify/{}".format(reference)
        headers = {
            "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        result = response.json()
        print('Paystack verify response:', result)  # Debug log

        if result.get('status') and result['data']['status'] == 'success':
            # Log the transaction
            transaction_log = f"Transaction ID: {result['data']['reference']}, Amount: {amount} KES, Status: Success, Date: {datetime.now()}"
            logging.info(transaction_log)
            print(f"Logged transaction: {transaction_log}")  # Debug log

            return jsonify({
                "status": "success",
                "transaction_id": result['data']['reference'],
                "amount": amount
            })
        else:
            return jsonify({
                "status": "error",
                "message": result.get('message', 'Transaction verification failed')
            }), 400

    except requests.RequestException as e:
        print('Request error:', str(e))  # Debug log
        return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as e:
        print('General error:', str(e))  # Debug log
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)