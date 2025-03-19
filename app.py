from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/config')
def get_config():
    return jsonify({
        "paystackPublicKey": os.getenv('PAYSTACK_PUBLIC_KEY')
    })

@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        data = request.get_json()
        reference = data.get('reference')
        amount = data.get('amount')  # Amount in KES from the front end
        if not reference or not amount:
            return jsonify({"status": "error", "message": "No reference or amount provided"}), 400

        # Verify transaction with Paystack
        url = "https://api.paystack.co/transaction/verify/{}".format(reference)
        headers = {
            "Authorization": f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        result = response.json()

        if result.get('status') and result['data']['status'] == 'success':
            return jsonify({
                "status": "success",
                "transaction_id": result['data']['reference'],
                "amount": amount  # Return the amount entered by the user
            })
        else:
            return jsonify({
                "status": "error",
                "message": result.get('message', 'Transaction verification failed')
            }), 400

    except requests.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)