from django.core.management.base import BaseCommand
from myapp.paypal_utils import create_paypal_product, create_paypal_subscription_plan

class Command(BaseCommand):
    help = "Create PayPal products and subscription plans"

    def handle(self, *args, **options):
        print("Successfully retrieved PayPal access token.")
    
        # Create the PayPal product first
        product_id = create_paypal_product()
    
        if product_id:
            # Define return and cancel URLs
            return_url = "https://www.iriseupacademy.com/complete-paypal-payment/"
            cancel_url = "https://www.iriseupacademy.com/payment/"
            
            # Create each subscription plan with updated amounts
            one_week_plan_id = create_paypal_subscription_plan(product_id, "1-week", "WEEK", 1, 1287, return_url, cancel_url)
            four_week_plan_id = create_paypal_subscription_plan(product_id, "4-week", "WEEK", 4, 3795, return_url, cancel_url)
            twelve_week_plan_id = create_paypal_subscription_plan(product_id, "12-week", "WEEK", 12, 9700, return_url, cancel_url)
            
            # Create a one-time payment plan for lifetime access
            lifetime_plan_id = create_paypal_subscription_plan(product_id, "lifetime", "YEAR", 1, 29700, return_url, cancel_url)

            
            # Print the created plan IDs
            print(f"Created Plan ID for 1-week: {one_week_plan_id}")
            print(f"Created Plan ID for 4-week: {four_week_plan_id}")
            print(f"Created Plan ID for 12-week: {twelve_week_plan_id}")
            print(f"Created Plan ID for Lifetime Access: {lifetime_plan_id}")
        else:
            print("Failed to create PayPal product.")
