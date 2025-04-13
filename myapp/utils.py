from django.shortcuts import render, redirect
from django.contrib import messages
from .models import EmailCollection  # Assuming you have an EmailCollection model
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import EmailCollection
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging
from .models import *
import logging
from django.utils.crypto import get_random_string 


def grant_course_access(user, selected_plan):
    """
    This function grants the user access to all courses and sets an expiration date based on the selected plan.
    """
    # Get all courses available in the course menu
    courses = Course.objects.all()

    # Set a default expiration date (optional)
    expiration_date = None

    # Determine expiration date based on selected plan
    if selected_plan == '1-week':
        expiration_date = timezone.now() + timedelta(weeks=1)
    elif selected_plan == '4-week':
        expiration_date = timezone.now() + timedelta(weeks=4)
    elif selected_plan == '12-week':
        expiration_date = timezone.now() + timedelta(weeks=12)
    else:
        # Handle the case where the selected plan is not recognized
        expiration_date = timezone.now() + timedelta(weeks=4)  # Default to 1 week if plan is unrecognized
        # Optionally, log a warning or handle this situation differently
        logger.warning(f"Unrecognized selected plan: {selected_plan}, defaulting to 4 week expiration.")

    # Grant access to all courses with the determined expiration date
    for course in courses:
        UserCourseAccess.objects.create(user=user, course=course, progress=0.0, expiration_date=expiration_date)

    return True


import msal
import os
import requests
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def get_graph_api_access_token():
    """
    Fetches an access token for Microsoft Graph API using the client credentials flow.
    """
    try:
        client_id = os.getenv("EMAIL_CLIENT_ID")
        #client_secret = os.getenv("EMAIL_CLIENT_SECRET")
        client_secret = os.getenv("EMAIL_CLIENT_SECRET")  # Replace with your actual secret value
        tenant_id = os.getenv("EMAIL_TENANT_ID")
        authority = f"https://login.microsoftonline.com/{tenant_id}"
        
        # Initialize the MSAL ConfidentialClientApplication
        app = msal.ConfidentialClientApplication(client_id, client_secret, authority=authority)
        
        # Acquire token for Graph API
        token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        
        if "access_token" in token_response:
            logger.info("Successfully acquired access token.")
            return token_response["access_token"]
        else:
            error_desc = token_response.get('error_description', 'No error description provided')
            raise Exception(f"Failed to acquire token: {error_desc}")
    except Exception as e:
        logger.error(f"Exception occurred while fetching Graph API token: {e}", exc_info=True)
        raise


import os
import requests
import logging
from myapp.utils import get_graph_api_access_token

logger = logging.getLogger(__name__)

def send_email_with_graph_api(to_email, subject, body, is_html=False):
    """
    Sends an email using Microsoft Graph API.
    """
    try:
        # Fetch access token
        access_token = get_graph_api_access_token()

        # Construct the email payload
        content_type = "HTML" if is_html else "Text"
        email_payload = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": content_type,
                    "content": body
                },
                "toRecipients": [
                    {"emailAddress": {"address": to_email}}
                ]
            }
        }

        # Send email
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            os.getenv("EMAIL_ENDPOINT"),
            json=email_payload,
            headers=headers
        )

        # Check the response
        if response.status_code == 202:
            logger.info(f"Email sent successfully to {to_email}.")
            return {"success": True}
        else:
            logger.error(f"Failed to send email to {to_email}: {response.text}")
            return {"success": False, "error": response.text}
    except Exception as e:
        logger.error(f"Exception occurred while sending email to {to_email}: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


from myapp.utils import send_email_with_graph_api
import logging

logger = logging.getLogger(__name__)

def send_renewal_email(user_email, expiration_date, selected_plan):
    """
    Sends a renewal confirmation email with HTML design to the user via Microsoft Graph API.
    """
    if not user_email or not expiration_date or not selected_plan:
        logger.error(f"Missing parameters for send_renewal_email: user_email={user_email}, "
                     f"expiration_date={expiration_date}, selected_plan={selected_plan}")
        return False

    subject = 'Your Subscription Has Been Renewed – Thank You for Staying with iRiseUp.AI!'

    # HTML content with modern design improvements
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{subject}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background-color: #05374f;
                color: #ffffff;
                padding: 20px;
                text-align: center;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: bold;
            }}
            .content {{
                padding: 30px 20px;
                text-align: left;
            }}
            .content p {{
                font-size: 16px;
                color: #333;
                line-height: 1.5;
            }}
            .content strong {{
                font-weight: bold;
                color: #05374f;
            }}
            .button {{
                display: inline-block;
                padding: 12px 25px;
                background-color: #05374f;
                color: #ffffff;
                text-decoration: none;
                font-size: 16px;
                border-radius: 5px;
                margin-top: 20px;
            }}
            .button:hover {{
                background-color: #007bb5;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                background-color: #f4f4f4;
                color: #888;
                font-size: 12px;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }}
            .footer p {{
                margin: 0;
            }}
            .footer a {{
                color: #05374f;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Email Header -->
            <div class="header">
                <h1>Subscription Renewal Confirmation</h1>
            </div>

            <!-- Email Content -->
            <div class="content">
                <p>Dear {user_email},</p>
                <p>Your subscription has been successfully renewed!</p>
                <p><strong>Plan:</strong> {selected_plan.capitalize()}</p>
                <p><strong>Next Expiration Date:</strong> {expiration_date.strftime('%B %d, %Y')}</p>
                <p>Thank you for choosing iRiseUp.AI! Our AI assistants are always ready to help you.</p>
                <a href="https://www.iriseup.ai/dashboard" class="button">Access Your Account</a>
                <p>Best regards,<br><strong>The iRiseUp.AI Team</strong></p>
            </div>

            <!-- Email Footer -->
            <div class="footer">
                <p>iRiseUp.AI, Columbus, Ohio, USA | <a href="https://www.iriseup.ai/unsubscribe">Unsubscribe</a></p>
            </div>
        </div>
    </body>
    </html>
    """

    # Send email using the utility function
    try:
        logger.debug("Preparing to send renewal email via Graph API.")
        response = send_email_with_graph_api(
            to_email=user_email,
            subject=subject,
            body=html_content,
            is_html=True
        )
        if response["success"]:
            logger.info(f"Renewal email sent successfully to {user_email}.")
            return True
        else:
            error_details = response.get("error", "Unknown error")
            logger.error(f"Failed to send renewal email to {user_email}: {error_details}")
            return False
    except Exception as e:
        logger.error(f"Exception occurred while sending renewal email to {user_email}: {e}", exc_info=True)
        return False


from django.core.mail import EmailMultiAlternatives

def send_failure_email(user_email, error_message):
    """
    Sends a failure notification email to the user when their renewal payment fails.
    """
    subject = 'Payment Renewal Failed – Action Required'
    from_email = 'iriseupgroupofcompanies@gmail.com'
    to_email = [user_email]

    # Plain text content for fallback
    text_content = (
        f"Dear {user_email},\n\n"
        "Unfortunately, we were unable to process your subscription renewal payment.\n"
        f"Error: {error_message}\n\n"
        "Please verify your payment information or contact support for assistance.\n\n"
        "Best regards,\n"
        "The iRiseUp.AI Team"
    )

    # HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Payment Renewal Failed</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{
                background-color: #ff4d4d;
                color: #ffffff;
                padding: 20px;
                text-align: center;
            }}
            .header img {{
                max-width: 100px;
                margin-bottom: 10px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
                font-weight: bold;
            }}
            .content {{
                padding: 30px 20px;
                text-align: left;
                background-color: #ffffff;
            }}
            .content p {{
                font-size: 16px;
                margin-bottom: 20px;
            }}
            .error-message {{
                font-size: 16px;
                font-weight: bold;
                color: #ff4d4d;
            }}
            .button {{
                display: inline-block;
                padding: 12px 25px;
                color: #ffffff;
                background-color: #05374f;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
                margin-top: 20px;
            }}
            .button:hover {{
                background-color: #007bb5;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                background-color: #f4f4f4;
                color: #888;
                font-size: 12px;
            }}
            .footer p {{
                margin: 0;
            }}
            .footer a {{
                color: #05374f;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Email Header -->
            <div class="header">
                <h1>Payment Renewal Failed</h1>
            </div>

            <!-- Email Content -->
            <div class="content">
                <p>Dear {user_email},</p>
                <p>Unfortunately, we encountered an issue while processing your subscription renewal payment.</p>
                <p class="error-message">Error: {error_message}</p>
                <p>Please verify your payment information or contact support for assistance.</p>
                <a href="https://www.iriseup.ai/contact-support" class="button">Contact Support</a>
                <p>Best regards,<br><strong>The iRiseUp.AI Team</strong></p>
            </div>

            <!-- Email Footer -->
            <div class="footer">
                <p>iRiseUp.AI, Columbus, Ohio, USA | <a href="https://www.iriseup.ai/unsubscribe">Unsubscribe</a></p>
            </div>
        </div>
    </body>
    </html>
    """

    # Create the email message with plain text and HTML alternatives
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()




import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import EmailMultiAlternatives
from .models import UserCourseAccess

def send_ezra_welcome_email(user_email, random_password):
    """
    Sends a personalized welcome email with HTML design to new Ezra users.
    """
    subject = 'Welcome to Ezra AI – Your Personal Success Companion!'
    from_email = 'iriseupgroupofcompanies@gmail.com'  # Update with your actual sender email
    to_email = [user_email]

    # Plain text fallback content
    text_content = (
        f"Hello {user_email},\n\n"
        "Welcome to Ezra AI! Your personal success companion is ready to assist you.\n"
        f"Here is your temporary password: {random_password}\n\n"
        "Please log in to update your password and begin your journey to success.\n\n"
        "Best regards,\n"
        "The Ezra AI Team"
    )

    # HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Welcome to Ezra AI</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                line-height: 1.6;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                background-color: #4e73df;
                color: #ffffff;
                padding: 20px;
                text-align: center;
            }}
            .content {{
                padding: 30px 20px;
                text-align: left;
                background-color: #ffffff;
            }}
            .content p {{
                font-size: 16px;
                margin-bottom: 20px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 25px;
                color: #ffffff;
                background-color: #4e73df;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
            }}
            .button:hover {{
                background-color: #375a7f;
            }}
            .footer {{
                text-align: center;
                padding: 15px;
                background-color: #f4f4f4;
                color: #888;
                font-size: 12px;
            }}
            .footer a {{
                color: #4e73df;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Email Header -->
            <div class="header">
                <h1>Welcome to Ezra AI, {user_email}!</h1>
            </div>

            <!-- Email Content -->
            <div class="content">
                <p>Hello {user_email},</p>
                <p>Your account has been successfully created. Below is your temporary password:</p>
                <p><strong>Temporary Password:</strong> {random_password}</p>
                <p>
                    Please log in to update your password and unlock the full potential of Ezra AI, 
                    your personal success companion.
                </p>
                <a href="https://www.iriseup.ai/sign_in" class="button">Log In Now</a>
                <p>Best regards,<br><strong>The Ezra AI Team</strong></p>
            </div>

            <!-- Email Footer -->
            <div class="footer">
                <p>Ezra AI | Columbus, Ohio, USA | <a href="https://iriseup.ai/unsubscribe">Unsubscribe</a></p>
            </div>
        </div>
    </body>
    </html>
    """

    # Create and send the email
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()



import openai

def generate_title_from_ai(ai_response):
    """Generate a short and relevant chat title based on AI's first response."""
    client = openai.OpenAI()
    title_response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can use GPT-4 if available
        messages=[
            {"role": "system", "content": "Create a very short title summarizing this conversation."},
            {"role": "user", "content": f"Summarize this in a title: {ai_response}"}
        ]
    )

    return title_response.choices[0].message.content.strip()


def detect_and_translate(message, target_lang="en"):
    """
    If the user requests translation (e.g., "Translate this to English"), this will handle that.
    Otherwise, the system will assume the language is as preferred.
    """
    try:
        # If the user does not explicitly ask for translation, just return the message
        if "translate" not in message.lower():
            return (target_lang, message)

        # For explicit translation requests, use OpenAI
        client = openai.OpenAI()
        system_msg = f"Translate the following message to {target_lang}:"
        prompt = f"{message}"

        # Request OpenAI to translate the message
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )

        translated = response.choices[0].message.content.strip()
        return (target_lang, translated)

    except Exception as e:
        logger.error(f"Translation error: {e}")
        return ("unknown", message)  # Fallback


# myapp/utils.py
from django.utils.translation import activate, get_language

def set_user_language(request, language_code):
    """
    Sets the user's language preference and stores it in the session.
    """
    # Activate the user's preferred language
    activate(language_code)
    # Store the language code in the session
    request.session['django_language'] = language_code

def get_user_language(request):
    """
    Retrieves the currently active language.
    """
    # Retrieve the current active language
    return get_language()


import openai
import logging

logger = logging.getLogger(__name__)

def is_translation_intended(message):
    """
    Uses OpenAI to determine if the user is asking for a translation.
    Returns True if translation is likely intended, False otherwise.
    """
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an intent detector. Reply with 'yes' if the user is "
                        "asking for a translation of a word, phrase, or message. Reply with 'no' otherwise. "
                        "Only say 'yes' or 'no'."
                    )
                },
                {"role": "user", "content": message}
            ],
            max_tokens=3
        )
        decision = response.choices[0].message.content.strip().lower()
        return "yes" in decision
    except Exception as e:
        logger.error(f"Intent detection failed: {e}")
        return False
