import requests
from requests.auth import HTTPBasicAuth
import logging


class PayPalClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US"
        }
        data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(url, headers=headers, data=data, auth=(self.client_id, self.client_secret))
        response.raise_for_status()
        access_token = response.json()['access_token']
        return access_token

    def get_order(self, order_id):
        url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def capture_order(self, order_id):
        url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{order_id}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()

