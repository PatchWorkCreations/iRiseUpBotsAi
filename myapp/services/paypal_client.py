# myapp/services/paypal_client.py

import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

class PayPalClient:
    def __init__(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.base_url = 'https://api-m.sandbox.paypal.com'  # Use 'https://api-m.paypal.com' for live

    def get_access_token(self):
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US",
        }
        data = {
            "grant_type": "client_credentials"
        }

        response = requests.post(url, headers=headers, data=data, auth=HTTPBasicAuth(self.client_id, self.client_secret))

        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception(f"Failed to obtain access token: {response.json()}")

    def capture_payment(self, authorization_id, amount):
        url = f"{self.base_url}/v2/payments/authorizations/{authorization_id}/capture"
        access_token = self.get_access_token()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        data = {
            "amount": {
                "value": amount,
                "currency_code": "USD"
            },
            "final_capture": True
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(f"Failed to capture payment: {response.json()}")
