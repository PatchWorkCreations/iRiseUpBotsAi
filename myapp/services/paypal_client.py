import requests
from requests.auth import HTTPBasicAuth

class PayPalClient:
    def __init__(self, client_id, client_secret):
        self.client_id = 'AcO0pQSFgkyRPtmmgviw2lz2DCojtl28Y_Qr9bligTeR1kOZScy9jecX2eWixffPBqGDJJyxSWn5iT__'
        self.client_secret = 'ELbhk0AXF3pOlgiJ378aXLtHzonT4EzPXkvQzEPv7dpTUth6GJOx_C6okSLpJmW2xf-ipC2zBCZzP0hQ'
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

    def capture_payment(self, authorization_id, amount):
        url = f"{self.base_url}/v2/payments/authorizations/{authorization_id}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}"
        }
        data = {
            "amount": {
                "value": amount,
                "currency_code": "USD"
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
