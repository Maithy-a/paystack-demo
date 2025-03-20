from flask import Flask, send_from_directory, request, jsonify
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    # Serve index.html
    return send_from_directory('..', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    # Serve other static files
    return send_from_directory('..', path)

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

        # Verify transaction
        url = "https://api.paystack.co/transaction/verify/{}".format(reference)
        headers = {
            "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        result = response.json()
        print('Paystack verify response:', result)  # Debug log

        if result.get('status') and result['data']['status'] == 'success':
            # Log to terminal for debugging
            transaction_log = f"Transaction ID: {result['data']['reference']}, Amount: {amount} KES, Status: Success"
            print(f"Processed transaction: {transaction_log}")  # Debug log

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