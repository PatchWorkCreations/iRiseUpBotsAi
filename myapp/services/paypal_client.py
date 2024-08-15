import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

class PayPalClient:
    def __init__(self, client_id, client_secret):
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.base_url = "https://api-m.sandbox.paypal.com"
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US"
        }
        data = {
            "grant_type": "client_credentials"
        }
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        
        response = requests.post(url, headers=headers, data=data, auth=auth)
        response.raise_for_status()
        return response.json()['access_token']

    def capture_order(self, order_id):
        url = f"{self.base_url}/v2/checkout/orders/{order_id}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()
