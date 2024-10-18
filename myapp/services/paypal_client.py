import requests
from requests.auth import HTTPBasicAuth
import logging
from time import time

logger = logging.getLogger(__name__)

class PayPalClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiry = None
        self.get_access_token()

    def get_access_token(self):
        url = "https://api-m.paypal.com/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US"
        }
        data = {
            "grant_type": "client_credentials"
        }
        response = requests.post(url, headers=headers, data=data, auth=(self.client_id, self.client_secret))
        response.raise_for_status()
        response_data = response.json()
        self.access_token = response_data['access_token']
        # Token expiry time is usually provided in seconds
        self.token_expiry = time() + response_data['expires_in'] - 60  # refresh 1 minute before actual expiry
        logger.info("Successfully retrieved PayPal access token.")

    def ensure_token_valid(self):
        if not self.access_token or time() >= self.token_expiry:
            logger.info("Access token expired or missing, refreshing token...")
            self.get_access_token()

    def get_headers(self):
        self.ensure_token_valid()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }

    def get_order(self, order_id):
        url = f"https://api-m.paypal.com/v2/checkout/orders/{order_id}"
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def capture_order(self, order_id):
        url = f"https://api-m.paypal.com/v2/checkout/orders/{order_id}/capture"
        headers = self.get_headers()
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()
