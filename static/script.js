// Fetch configuration from backend
async function fetchConfig() {
    const response = await fetch('/config');
    return await response.json();
}

async function initializePaystack() {
    const config = await fetchConfig();
    const paystack = window.PaystackPop.setup({
        key: config.paystackPublicKey,
        callback: function(response) {
            processPayment(response.reference, document.getElementById('amount').value);
        },
        onClose: function() {
            const resultDiv = document.getElementById('result');
            resultDiv.innerText = 'Payment cancelled.';
            resultDiv.className = 'error';
        }
    });

    document.getElementById('pay-button').addEventListener('click', function() {
        const amount = document.getElementById('amount').value;
        const cardNumber = document.getElementById('card-number').value;
        const expiry = document.getElementById('expiry').value;
        const cvv = document.getElementById('cvv').value;
        const email = document.getElementById('email').value;

        const resultDiv = document.getElementById('result');
        if (!amount || !cardNumber || !expiry || !cvv || !email) {
            resultDiv.innerText = 'All fields are required.';
            resultDiv.className = 'error';
            return;
        }

        // Convert amount to kobo (smallest unit for KES)
        const amountInKobo = parseFloat(amount) * 100;

        paystack.checkCard({
            cardNumber: cardNumber,
            expiryMonth: expiry.split('/')[0],
            expiryYear: expiry.split('/')[1],
            cvv: cvv
        }, function(response) {
            if (response.status) {
                paystack.options.amount = amountInKobo; // Dynamically set amount
                paystack.options.email = email; // Dynamically set email
                paystack.openIframe();
            } else {
                resultDiv.innerText = 'Invalid card details.';
                resultDiv.className = 'error';
            }
        });
    });
}

function processPayment(reference, amount) {
    fetch('/process_payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ reference: reference, amount: amount })
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        if (data.status === 'success') {
            resultDiv.innerText = `Transaction successful! ID: ${data.transaction_id}, Amount: ${data.amount} KES`;
            resultDiv.className = 'success';
        } else {
            resultDiv.innerText = 'Transaction failed: ' + data.message;
            resultDiv.className = 'error';
        }
    })
    .catch(err => {
        console.error('Error processing payment:', err);
        const resultDiv = document.getElementById('result');
        resultDiv.innerText = 'Error contacting server.';
        resultDiv.className = 'error';
    });
}

// Initialize Paystack
document.addEventListener('DOMContentLoaded', initializePaystack);