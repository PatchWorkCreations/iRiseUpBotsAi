from django.core.management.base import BaseCommand
from myapp.paypal_utils import create_paypal_product, create_paypal_subscription_plan

class Command(BaseCommand):
    help = "Create PayPal products and subscription plans"

    def handle(self, *args, **options):
      print("Successfully retrieved PayPal access token.")
    
    # Create the PayPal product first
    product_id = create_paypal_product()
    
    if product_id:
        # Create each subscription plan
        one_week_plan_id = create_paypal_subscription_plan(product_id, "1-week", "WEEK", 1, 1386)
        four_week_plan_id = create_paypal_subscription_plan(product_id, "4-week", "WEEK", 4, 3999)
        twelve_week_plan_id = create_paypal_subscription_plan(product_id, "12-week", "WEEK", 12, 7999)
        
        # Print the created plan IDs
        print(f"Created Plan ID for 1-week: {one_week_plan_id}")
        print(f"Created Plan ID for 4-week: {four_week_plan_id}")
        print(f"Created Plan ID for 12-week: {twelve_week_plan_id}")
    else:
        print("Failed to create PayPal product.")


