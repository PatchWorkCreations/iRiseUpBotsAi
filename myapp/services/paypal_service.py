# yourapp/services/paypal_service.py
import requests
from django.conf import settings

PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com"

class PayPalService:
    def __init__(self):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.access_token = self.get_access_token()

    def get_access_token(self):
        auth_response = requests.post(
            f"{PAYPAL_API_BASE}/v1/oauth2/token",
            headers={
                "Accept": "application/json",
                "Accept-Language": "en_US",
            },
            data={
                "grant_type": "client_credentials",
            },
            auth=(self.client_id, self.client_secret),
        )
        auth_response.raise_for_status()
        return auth_response.json()["access_token"]

    def capture_payment(self, authorization_id, amount, currency="USD"):
        capture_url = f"{PAYPAL_API_BASE}/v2/payments/authorizations/{authorization_id}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        capture_response = requests.post(
            capture_url,
            headers=headers,
            json={
                "amount": {
                    "currency_code": currency,
                    "value": amount,
                },
                "final_capture": True,
            },
        )
        capture_response.raise_for_status()
        return capture_response.json()
