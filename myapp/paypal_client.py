import requests
import logging

class PayPalClient:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        logging.info(f"PayPal Client ID: {self.client_id}")
        logging.info(f"PayPal Client Secret: {self.client_secret[:4]}****")  # Hide most of the secret for safety
        self.access_token = self.get_access_token()


    def get_access_token(self):
        url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US",
        }
        data = {
            "grant_type": "client_credentials"
        }

        try:
            logging.info("Requesting PayPal access token...")
            response = requests.post(url, headers=headers, data=data, auth=(self.client_id, self.client_secret))
            response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
            access_token = response.json().get("access_token")
            if not access_token:
                logging.error("Failed to retrieve access token from PayPal response.")
                raise ValueError("Access token not found in response.")
            logging.info("Successfully retrieved PayPal access token.")
            return access_token

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            logging.error(f"Response content: {response.text}")
            raise

        except Exception as err:
            logging.error(f"An error occurred: {err}")
            raise
