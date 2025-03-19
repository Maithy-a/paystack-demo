// Fetch configuration from backend
async function fetchConfig() {
    try {
        const response = await fetch('/config');
        if (!response.ok) throw new Error('Failed to fetch config');
        return await response.json();
    } catch (error) {
        console.error('Error fetching config:', error);
        throw error;
    }
}

async function initializePaystack() {
    try {
        const config = await fetchConfig();
        console.log('Config loaded:', config);

        document.getElementById('pay-button').addEventListener('click', function(event) {
            event.preventDefault(); // Prevent submission

            const amount = document.getElementById('amount').value;
            const email = document.getElementById('email').value;

            const resultDiv = document.getElementById('result');
            if (!amount || !email) {
                resultDiv.innerText = 'Amount and email are required.';
                resultDiv.className = 'error';
                return;
            }

            // Convert currency to KES
            const amountInKobo = Math.round(parseFloat(amount) * 100);
            if (isNaN(amountInKobo) || amountInKobo <= 0) {
                resultDiv.innerText = 'Invalid amount.';
                resultDiv.className = 'error';
                return;
            }

            // Initialize Paystack 
            const paystack = window.PaystackPop.setup({
                key: config.paystackPublicKey,
                email: email,
                amount: amountInKobo,
                currency: 'KES',
                callback: function(response) {
                    console.log('Paystack callback response:', response);
                    processPayment(response.reference, amount);
                },
                onClose: function() {
                    console.log('Paystack popup closed');
                    resultDiv.innerText = 'Payment cancelled.';
                    resultDiv.className = 'error';
                }
            });

            // Open Paystack popup
            paystack.openIframe();
        });
    } catch (error) {
        const resultDiv = document.getElementById('result');
        resultDiv.innerText = 'Error initializing Paystack: ' + error.message;
        resultDiv.className = 'error';
    }
}

function processPayment(reference, amount) {
    fetch('/process_payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ reference: reference, amount: amount })
    })
    .then(response => {
        console.log('Process payment response status:', response.status);
        if (!response.ok) throw new Error('Failed to process payment');
        return response.json();
    })
    .then(data => {
        const resultDiv = document.getElementById('result');
        console.log('Process payment response data:', data);
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
        resultDiv.innerText = 'Error contacting server: ' + err.message;
        resultDiv.className = 'error';
    });
}

// Initialize Paystack
document.addEventListener('DOMContentLoaded', async () => {
    if (typeof PaystackPop === 'undefined') {
        const resultDiv = document.getElementById('result');
        resultDiv.innerText = 'Paystack library failed to load. Please check your internet connection.';
        resultDiv.className = 'error';
        return;
    }
    await initializePaystack();
});