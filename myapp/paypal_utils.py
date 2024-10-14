# myapp/paypal_utils.py

import requests  # For making HTTP requests
import uuid  # For generating unique request IDs
from django.conf import settings  # To access Django settings

# Import your PayPal client class
from .paypal_client import PayPalClient  

# Initialize the PayPal client with the client ID and secret from settings
paypal_client = PayPalClient(
    client_id=settings.PAYPAL_CLIENT_ID,
    client_secret=settings.PAYPAL_CLIENT_SECRET
)


def create_paypal_product():
    # Define the API endpoint and headers
    url = "https://api-m.sandbox.paypal.com/v1/catalogs/products"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {paypal_client.access_token}",
        "PayPal-Request-Id": str(uuid.uuid4())  # Unique ID for idempotency
    }

    # Define the payload for the product creation
    data = {
        "name": "AI-Powered Learning Program",  # The name of your product
        "description": "An AI-driven program designed to help you master AI tools, boost your income, and gain new digital skills.",  # A brief description of your product
        "type": "SERVICE",  # Since you're offering a subscription-based service
        "category": "SOFTWARE",  # Replace with a valid PayPal category
        "home_url": "https://iriseupai-production.up.railway.app/"  # Link to your main homepage or landing page
    }

    # Make the request to PayPal API
    response = requests.post(url, headers=headers, json=data)

    # Log full response if it is not JSON
    if response.headers.get('Content-Type') != 'application/json':
        print(f"Received non-JSON response: {response.text}")
        return None

    # Handle JSON parsing safely
    try:
        product_response = response.json()
    except ValueError as e:
        print(f"Failed to parse JSON: {response.text}")
        return None

    if response.status_code == 201:
        product_id = product_response.get("id")
        print(f"Successfully created PayPal product with ID: {product_id}")
        return product_id
    else:
        print(f"Failed to create PayPal product: {product_response}")
        return None
    
def create_paypal_subscription_plan(product_id, plan_name, interval_unit, interval_count, amount, return_url, cancel_url):
    url = "https://api-m.sandbox.paypal.com/v1/billing/plans"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {paypal_client.access_token}",
        "PayPal-Request-Id": str(uuid.uuid4())
    }

    total_cycles = 1 if plan_name == 'lifetime' else 0  # Set to 1 for lifetime, 0 for other plans (0 means indefinite)
    
    data = {
        "product_id": product_id,
        "name": f"{plan_name} Plan",
        "description": f"Subscription to {plan_name} plan",
        "billing_cycles": [
            {
                "frequency": {
                    "interval_unit": interval_unit,  # "WEEK", "MONTH", or "YEAR" for lifetime
                    "interval_count": interval_count  # e.g., 1 for 1-week or 4 for 4-week
                },
                "tenure_type": "REGULAR",
                "sequence": 1,
                "total_cycles": total_cycles,  # Only one cycle for lifetime plan
                "pricing_scheme": {
                    "fixed_price": {
                        "value": f"{amount/100:.2f}",  # Convert cents to dollars
                        "currency_code": "USD"
                    }
                }
            }
        ],
        "payment_preferences": {
            "auto_bill_outstanding": True if plan_name != 'lifetime' else False,  # No auto-bill for lifetime plan
            "setup_fee": {
                "value": "0",
                "currency_code": "USD"
            },
            "setup_fee_failure_action": "CONTINUE",
            "payment_failure_threshold": 3
        },
        "taxes": {
            "percentage": "10",
            "inclusive": False
        },
        "application_context": {
            "return_url": "https://iriseupai-production.up.railway.app/complete-paypal-payment/",
            "cancel_url": "https://iriseupai-production.up.railway.app/payment/"
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.headers.get('Content-Type') != 'application/json':
        print(f"Received non-JSON response: {response.text}")
        return None

    try:
        plan_response = response.json()
    except ValueError as e:
        print(f"Failed to parse JSON: {response.text}")
        return None

    response.raise_for_status()
    plan_id = plan_response.get("id")
    print(f"Created Plan ID for {plan_name}: {plan_id}")
    return plan_id

