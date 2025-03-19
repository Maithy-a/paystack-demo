# Paystack Demo Documentation
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)<br>
This documentation provides an overview of the Paystack Demo web application, which demonstrates Paystack payment integration in test mode. It includes setup instructions, testing guidelines, and notes for real implementation.

## Features
- Demonstrates Paystack payment integration in test mode.
- Supports KES (Kenyan Shilling) as the currency.
- Provides test card details for simulating payment scenarios.

## Setup Instructions
1. Install Python 3.x.
2. Install dependencies using `pip install -r requirements.txt`.
3. Obtain Paystack test API keys from the Paystack Dashboard.
4. Create a `.env` file to store API keys securely.Add the following and replace values:

    `PAYSTACK_PUBLIC_KEY`=pk_test_your_public_key_here<br>
    `PAYSTACK_SECRET_KEY`=sk_test_your_secret_key_here

5. **Run the Server**: Execute `python app.py`.
6. **Access the App**: Open `http://localhost:5000` in a browser.

## Notes
- Runs in Paystack test mode; no real payments are processed.
- Secrets are stored in `.env` and ignored by Git via `.gitignore`.
- Requires internet for Paystack API.
- Uses KES currency for Kenya.

## Real Implementation
- Use live Paystack keys for real transactions.
- Use HTTPS in production.

