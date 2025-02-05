from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    PasswordChangeView,
    PasswordChangeDoneView
)
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import datetime, timedelta
import logging
import requests
import uuid
import json

from myapp.forms import CustomPasswordResetForm, SubmitRequestForm, CustomPasswordChangeForm
from myapp.models import EmailCollection, Course, UserCourseAccess, KnowledgeBaseCategory, KnowledgeBaseArticle, KnowledgeBaseSubCategory
from myapp.services.paypal_client import PayPalClient
from square.client import Client
from django.shortcuts import render, get_object_or_404
from .models import Lesson, SubCourse, UserSubCourseAccess
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def about(request):
    return render(request, 'myapp/about.html')

def index(request):
    return render(request, 'myapp/index.html')

def index2(request):
    return render(request, 'myapp/index2.html')

def index3(request):
    return render(request, 'myapp/index3.html')

def blogclassic(request):
    return render(request, 'myapp/blog-classic.html')

def blog(request):
    return render(request, 'myapp/blog.html')



def faq(request):
    return render(request, 'myapp/faq.html')

from myapp.models import BlogPost

def index2(request):
    recent_blogs = BlogPost.objects.all().order_by('-publish_date')[:3]  # Fetch 3 most recent
    return render(request, 'myapp/index-2.html', {'recent_blogs': recent_blogs})

@login_required
def profile_view(request):
    user = request.user

    context = {
        'username': user.username if user.is_authenticated else "Guest",
        'email': user.email if user.is_authenticated else "Not available",
    }

    return render(request, 'myapp/course_list/profile.html', context)

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'myapp/course_list/course_list.html', {'courses': courses})


from django.shortcuts import render
from myapp.models import Course, UserCourseAccess, UserLessonProgress
from django.core.paginator import Paginator
from django.db.models import Prefetch

from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect
from myapp.models import UserCourseAccess

# Centralized product-to-dashboard mapping
DASHBOARD_ROUTES = {
    "414255": "elevate_dashboard",
    "414273": "thrive_dashboard",
    "414195": "lumos_dashboard",
    "414223": "imagine_dashboard",
    "414260": "gideon_dashboard",
    "414301": "mentor_iq_dashboard",
    "414302": "nexus_dashboard",
    "414303": "keystone_dashboard",
}

@login_required
def coursemenu(request):
    """
    Redirect users to their respective dashboards based on their product ID.
    If no product ID is associated, render the course menu.
    """
    user = request.user
    access = UserCourseAccess.objects.filter(user=user, is_active=True).first()

    if access:
        product_id = access.product_id
        dashboard_name = DASHBOARD_ROUTES.get(product_id)
        if dashboard_name:
            return redirect(dashboard_name)

    # Fallback: Render course menu if no valid access or product ID
    return render(request, 'myapp/aibots/coursemenu.html')


def subscription_terms_new(request):
    return render(request, 'myapp/aibots/subscription_terms.html')

def terms_and_conditions(request):
    return render(request, 'myapp/aibots/terms_and_conditions.html')

def data_privacy(request):
    return render(request, 'myapp/aibots/data_privacy.html')

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from myapp.models import Course, UserCourseAccess

@login_required
def toggle_favorite(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course_access, created = UserCourseAccess.objects.get_or_create(user=request.user, course=course)
    
    # Toggle the favorite status
    course_access.is_favorite = not course_access.is_favorite
    course_access.save()

    return redirect('course_detail', course_id=course.id)

@login_required
def toggle_save(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course_access, created = UserCourseAccess.objects.get_or_create(user=request.user, course=course)
    
    # Toggle the saved status
    course_access.is_saved = not course_access.is_saved
    course_access.save()

    return redirect('course_detail', course_id=course.id)


from django.shortcuts import redirect

def course_continue(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.is_authenticated:
        user_access = UserCourseAccess.objects.filter(user=request.user, course=course).first()
        if user_access and not user_access.has_expired():
            return render(request, 'myapp/course_detail.html', {'course': course})
        else:
            return redirect('coursemenu')  # Redirect to course menu if access is denied
    return render(request, 'myapp/course_detail.html', {'course': course})


def personalized_plan(request):
    if request.method == 'POST':
        gender = request.POST.get('gender')
        special_goal = request.POST.get('special_goal')
        main_goal = request.POST.get('main_goal')
        
        # Store data in the session
        if gender:
            request.session['gender'] = gender
        if special_goal:
            request.session['special_goal'] = special_goal
        if main_goal:
            request.session['main_goal'] = main_goal
        
        return redirect('next_view_name')  # Replace 'next_view_name' with the actual view name you want to redirect to

    # If the request is GET, render the template with the current session data
    gender = request.session.get('gender', '')
    special_goal = request.session.get('special_goal', '')
    main_goal = request.session.get('main_goal', '')
    
    context = {
        'gender': gender,
        'special_goal': special_goal,
        'main_goal' : main_goal,
    }

    return render(request, 'myapp/aibots/personalized_plan.html', context)


# Initialize the Square Client
square_client = Client(
    access_token=settings.SQUARE_ACCESS_TOKEN,
    environment='production',
)

def setSelectedPlanInSession(request):
    selected_plan = request.POST.get('plan')
    logger.info(f"Selected plan: {selected_plan}")  # Log the plan value received
    allowed_plans = ['1-week', '4-week', '12-week', 'lifetime']

    if selected_plan not in allowed_plans:
        logger.error(f"Invalid plan selected: {selected_plan}")  # Log the invalid plan case
        return JsonResponse({'success': False, 'error': 'Invalid plan selected.'})

    request.session['selected_plan'] = selected_plan
    return JsonResponse({'success': True})


def determine_amount_based_on_plan(selected_plan):
    if selected_plan == '1-week':
        return 100  # $12.87 in cents
    elif selected_plan == '4-week':
        return 3795  # $37.95 in cents
    elif selected_plan == '12-week':
        return 9700  # $97.00 in cents
    elif selected_plan == 'lifetime':
        return 24700  # $247.00 in cents
    else:
        return 0  # Default to 0 for unrecognized plans



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
    elif selected_plan == 'lifetime':
        expiration_date = None 
    else:
        # Handle the case where the selected plan is not recognized
        expiration_date = timezone.now() + timedelta(weeks=4)  # Default to 1 week if plan is unrecognized
        # Optionally, log a warning or handle this situation differently
        logger.warning(f"Unrecognized selected plan: {selected_plan}, defaulting to 4 week expiration.")

    # Grant access to all courses with the determined expiration date
    for course in courses:
        UserCourseAccess.objects.create(user=user, course=course, progress=0.0, expiration_date=expiration_date)

    return True


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailCollection  # Assuming you have an EmailCollection model

def email_collection(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        receive_offers = request.POST.get('receive_offers') == 'on'

        if not email:
            messages.error(request, "Email cannot be empty.")
            return render(request, 'myapp/quiz/email_collection.html', {
                'receive_offers': receive_offers,
            })

        # Check if the email already exists
        email_collection, created = EmailCollection.objects.get_or_create(
            email=email,
            defaults={'receive_offers': receive_offers}
        )

        if not created:
            messages.error(request, "This email is already registered. Please use a different email or log in.")
            return render(request, 'myapp/quiz/email_collection.html', {
                'email': email,
                'receive_offers': receive_offers,
            })

        # Send the welcome email synchronously
        subject = 'Welcome to iRiseUp.ai!'
        html_message = render_to_string('welcome_email.html', {'email': email})
        plain_message = strip_tags(html_message)
        from_email = 'hello@iriseupacademy.com'  # Replace with your actual sender email
        send_mail(subject, plain_message, from_email, [email], html_message=html_message)

        # Store the email in the session for later use during payment
        request.session['email'] = email

        return redirect('personalized_plan')

    return render(request, 'myapp/quiz/email_collection.html')


from django.core.mail import EmailMultiAlternatives



def send_welcomepassword_email(user_email, random_password):
    """
    Sends a personalized welcome email with HTML design to new users.
    """
    subject = 'Welcome to iRiseUp.AI – Your Intelligent Assistant is Ready!'
    from_email = 'hello@iriseupacademy.com'
    to_email = [user_email]

    # Plain text content for fallback
    text_content = (
        f"Dear {user_email},\n\n"
        "Welcome to iRiseUp.AI! Your account has been successfully created.\n"
        f"Here is your temporary password: {random_password}\n\n"
        "Please log in to update your password and explore our intelligent AI assistants.\n\n"
        "Best regards,\n"
        "The iRiseUp.AI Team"
    )

    # HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Welcome to iRiseUp.AI</title>
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
                background-color: #05374f;
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
                <h1>Welcome to iRiseUp.AI, {user_email}!</h1>
            </div>

            <!-- Email Content -->
            <div class="content">
                <p>Hello {user_email},</p>
                <p>Your account has been successfully created. Below is your temporary password:</p>
                <p><strong>Temporary Password:</strong> {random_password}</p>
                <p>Please log in to update your password and unlock the full potential of iRiseUp.AI, where your team of AI assistants are ready to help streamline your work.</p>
                <a href="https://www.iriseup.ai/sign_in" class="button">Log In Now</a>
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





# Get an instance of a logger
logger = logging.getLogger('myapp')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
import json
import uuid
import logging
from square.client import Client
from .models import User  # Adjust according to your user model
from django.contrib.auth.models import User  # For User model
from django.utils.crypto import get_random_string  # For generating random passwords
from django.core.mail import send_mail  # For sending emails
from .models import SquareCustomer, User, UserCourseAccess

logger = logging.getLogger(__name__)

# Initialize Square client
client = Client(
    access_token=settings.SQUARE_ACCESS_TOKEN,
    environment='production',  # Change to 'production' when you're ready
)


@csrf_exempt
def process_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            card_token = data.get('source_id')
            selected_plan = data.get('plan')
            verification_token = data.get('verification_token')

            # Ensure the correct email is being used from the user's current session
            user_email = data.get('email')
            if not user_email:
                logger.error("Email is missing from session. Cannot proceed with payment.")
                return JsonResponse({"error": "Email is missing from session."}, status=400)
            
            first_name = data.get('firstName', '') or 'Unknown'  # Fallback if not provided
            last_name = data.get('lastName', '') or 'User'

            # Ensure the amount is valid based on the selected plan
            amount = determine_amount_based_on_plan(selected_plan)
            if amount <= 0:
                return JsonResponse({"error": "Invalid plan selected."}, status=400)

            # Step 1: Create a new customer or retrieve the existing one
            customer_result = square_client.customers.create_customer(
                body={
                    "given_name": first_name,
                    "family_name": last_name,
                    "email_address": user_email,
                }
            )
            if customer_result.is_error():
                logger.error("Customer creation failed: %s", customer_result.errors)
                user = User.objects.get(email=user_email)  # Assuming the user exists
                Transaction.objects.create(
                    user=user,
                    amount=amount,
                    subscription_type=selected_plan,
                    status='error',
                    error_logs=str(customer_result.errors),
                    recurring=False
                )
                return JsonResponse({"error": "Failed to create customer profile."}, status=400)

            customer_id = customer_result.body['customer']['id']

            # Step 2: Make the payment request with the verification token and store the card on file
            payment_result = square_client.payments.create_payment(
                body={
                    "source_id": card_token,
                    "idempotency_key": str(uuid.uuid4()),
                    "amount_money": {
                        "amount": amount,
                        "currency": "USD"
                    },
                    "verification_token": verification_token,
                    "autocomplete": True,
                    "customer_id": customer_id,  # Link the payment to the customer
                }
            )
            logger.info("Square API Payment Response: %s", payment_result)

            # Error handling for specific payment errors
            if payment_result.is_error():
                error_codes = [error['code'] for error in payment_result.errors]
                logger.error("Payment Error: %s", error_codes)

                if 'INSUFFICIENT_FUNDS' in error_codes:
                    return JsonResponse({"error": "Payment failed due to insufficient funds. Please ensure adequate balance and try again."}, status=400)
                elif 'CARD_DECLINED' in error_codes:
                    return JsonResponse({"error": "Your card was declined. Please try another payment method."}, status=400)
                elif 'INVALID_CARD' in error_codes:
                    return JsonResponse({"error": "Invalid card details. Please check and try again."}, status=400)
                elif 'EXPIRED_CARD' in error_codes:
                    return JsonResponse({"error": "Your card has expired. Please use another card."}, status=400)
                elif 'FRAUD_REJECTED' in error_codes:
                    return JsonResponse({"error": "Payment rejected due to suspected fraud. Please contact your bank."}, status=400)
                elif 'AUTHENTICATION_REQUIRED' in error_codes:
                    return JsonResponse({"error": "Additional authentication required. Please complete the verification."}, status=400)
                else:
                    # General error for other cases
                    return JsonResponse({"error": "Payment failed. Please try again."}, status=400)

            payment_id = payment_result.body['payment']['id']

            # Step 3: Store the card on file for the customer
            card_result = square_client.cards.create_card(
                body={
                    "idempotency_key": str(uuid.uuid4()),
                    "source_id": payment_id,
                    "verification_token": verification_token,
                    "card": {
                        "cardholder_name": f"{data.get('givenName')} {data.get('familyName')}",
                        "customer_id": customer_id,
                    }
                }
            )
            if card_result.is_error():
                logger.error("Card storage failed: %s", card_result.errors)
                Transaction.objects.create(
                    user=user,
                    amount=amount,
                    subscription_type=selected_plan,
                    status='error',
                    error_logs=str(card_result.errors),
                    recurring=False
                )
                return JsonResponse({"error": "Failed to store card on file."}, status=400)

            card_id = card_result.body['card']['id']

            # Step 4: Create or retrieve the user in the Django application
            # Update or create the user with username set to email, adding first and last name support
            user, created = User.objects.get_or_create(
                username=user_email,
                defaults={
                    'email': user_email,
                    'first_name': first_name,
                    'last_name': last_name
                }
            )

            # If the user already exists (not created), update their first and last names if they’re missing
            if not created:
                if not user.first_name:
                    user.first_name = first_name
                if not user.last_name:
                    user.last_name = last_name
                user.save()


            if created:
                random_password = get_random_string(8)
                user.set_password(random_password)
                user.save()

                # Send the welcome email
                send_welcomepassword_email(user_email, random_password)

            logger.info(f"User {user_email} processed for payment.")


            # Step 6: Store the customer_id and card_id in the database
            SquareCustomer.objects.update_or_create(
                user=user,
                defaults={'customer_id': customer_id, 'card_id': card_id}
            )

            # Step 7: Compute expiration date and next billing date
            expiration_date = None
            next_billing_date = None
            if selected_plan == '1-week':
                expiration_date = timezone.now() + timedelta(weeks=1)
                next_billing_date = expiration_date
            elif selected_plan == '4-week':
                expiration_date = timezone.now() + timedelta(weeks=4)
                next_billing_date = expiration_date
            elif selected_plan == '12-week':
                expiration_date = timezone.now() + timedelta(weeks=12)
                next_billing_date = expiration_date
            elif selected_plan == 'lifetime':
                expiration_date = None  # No expiration
                next_billing_date = None  # No recurring billing for lifetime

            # Update UserCourseAccess for lifetime plan
            UserCourseAccess.objects.update_or_create(
                user=user,
                defaults={
                    'expiration_date': expiration_date,
                    'selected_plan': selected_plan
                }
            )

            # Step 9: Create a transaction with a success status and recurring info
            Transaction.objects.create(
                user=user,
                amount=amount,
                subscription_type=selected_plan,
                status='success',
                recurring=True if selected_plan in ['1-week', '4-week', '12-week'] else False,
                next_billing_date=next_billing_date  # Store the next billing date
            )

            return JsonResponse({"success": True})

        except Exception as e:
            logger.error("Unexpected error occurred: %s", str(e), exc_info=True)
            user = User.objects.get(email=user_email) if 'user_email' in locals() else None
            if user:
                Transaction.objects.create(
                    user=user,
                    amount=amount,
                    subscription_type=selected_plan,
                    status='error',
                    error_logs=str(e),
                    recurring=False
                )
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


# Initialize the logger
logger = logging.getLogger(__name__)


def payment_page(request):
    return render(request, 'myapp/quiz/process_payment.html')

def success_page(request):
    return render(request, 'myapp/quiz/success.html', {"message": "Subscription completed successfully."})



def subscription_terms(request):
    return render(request, 'myapp/quiz/subscription_terms.html')

def terms_conditions(request):
    return render(request, 'myapp/quiz/terms_conditions.html')

def privacy_policy(request):
    return render(request, 'myapp/quiz/privacy_policy.html')  # Privacy Policy view

def support_center(request):
    # Get all categories
    categories = KnowledgeBaseCategory.objects.prefetch_related('subcategories__articles').all()

    # Get articles marked as popular
    popular_articles = KnowledgeBaseArticle.objects.filter(is_popular=True)  # Assuming 'is_popular' is a boolean field in KnowledgeBaseArticle

    context = {
        'categories': categories,
        'popular_articles': popular_articles,
    }
    return render(request, 'myapp/quiz/support/support_center.html', context)


def knowledge_base(request):
    categories = KnowledgeBaseCategory.objects.prefetch_related('subcategories__articles').all()
    return render(request, 'myapp/quiz/support/knowledge_base.html', {'categories': categories})


def subcategory_detail(request, id):
    subcategory = get_object_or_404(KnowledgeBaseSubCategory, id=id)
    articles = subcategory.articles.all()
    return render(request, 'myapp/quiz/support/subcategory_detail.html', {'subcategory': subcategory, 'articles': articles})


def article_detail(request, article_id):
    article = get_object_or_404(KnowledgeBaseArticle, id=article_id)
    try:
        article.content_parsed = json.loads(article.content)
    except json.JSONDecodeError:
        article.content_parsed = []
    same_subcategory_articles = KnowledgeBaseArticle.objects.filter(
        subcategory=article.subcategory
    ).exclude(id=article.id)

    # Optionally, get related articles from other subcategories
    related_articles = KnowledgeBaseArticle.objects.exclude(
        subcategory=article.subcategory
    ).exclude(id=article.id)[:4]  # Limit to 4 related articles

    return render(request, 'myapp/quiz/support/article_detail.html', {
        'article': article,
        'same_subcategory_articles': same_subcategory_articles,
        'related_articles': related_articles,
    })


def category_detail(request, id):
    category = get_object_or_404(KnowledgeBaseCategory, id=id)
    
    # Get all subcategories for this category
    subcategories = category.subcategories.all()
    
    # Get all articles under all subcategories of this category
    articles = KnowledgeBaseArticle.objects.filter(subcategory__in=subcategories)
    
    context = {
        'category': category,
        'subcategories': subcategories,
        'articles': articles,
    }
    return render(request, 'myapp/quiz/support/category_detail.html', context)



def preview_email(request):
    user_email = 'test@example.com'  # Example email, you can customize this
    return render(request, 'welcome_email.html', {'user_email': user_email})



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignInForm
from .models import UserCourseAccess
from django.conf import settings
import logging
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)
def sign_in(request):
    if request.user.is_authenticated:
        logger.debug(f"User {request.user.username} tried to access the login page while already logged in.")
        return redirect_to_user_ai(request.user)

    if request.method == 'POST':
        form = SignInForm(request.POST)

        if form.is_valid():
            login_identifier = form.cleaned_data.get('login_identifier')
            password = form.cleaned_data.get('password')
            logger.debug(f"Attempting login for identifier: {login_identifier}")

            # Authenticate using username or email
            user = authenticate(request, email=login_identifier, password=password)

            if user is None:
                # Try finding by email if username authentication fails
                try:
                    user = User.objects.get(email=login_identifier)
                    if user.check_password(password):
                        if not user.is_active:
                            user.is_active = True
                            user.save()
                            logger.info(f"Account reactivated for user: {user.username}")
                            messages.info(request, 'Your account has been reactivated.')
                        login(request, user)
                        logger.debug(f"Redirecting to user AI for reactivated user: {user.username}")
                        return redirect_to_user_ai(user)
                except User.DoesNotExist:
                    user = None

            if user is not None and user.is_active:
                # Check if last_login is NULL
                if user.last_login is None:
                    logger.debug(f"First login detected for user: {user.username}")
                    login(request, user)  # Log the user in before redirecting
                    messages.info(request, 'Please change your password to continue.')
                    return redirect('password_change')
                else:
                    login(request, user)
                    logger.debug(f"Redirecting to user AI for user: {user.username}")
                    messages.success(request, f'Welcome back, {user.first_name}!')
                    return redirect_to_user_ai(user)
            else:
                logger.error(f"Authentication failed for identifier: {login_identifier}")
                messages.error(request, 'Invalid username/email or password. Please try again.')
                return redirect('sign_in')

    else:
        form = SignInForm()

    return render(request, 'myapp/quiz/sign_in.html', {'form': form})

from django.shortcuts import redirect
from myapp.models import UserCourseAccess

def redirect_to_dashboard(user):
    """
    Redirect the user to their respective dashboard based on their product ID.
    """
    access = UserCourseAccess.objects.filter(user=user, is_active=True).first()
    if access:
        product_id = access.product_id
        if product_id == "414255":
            return redirect('elevate_dashboard')
        elif product_id == "414273":
            return redirect('thrive_dashboard')
        elif product_id == "414195":
            return redirect('lumos_dashboard')
        elif product_id == "414223":
            return redirect('imagine_dashboard')
        elif product_id == "414260":
            return redirect('gideon_dashboard')
        elif product_id == "kash":  # Example if kash has no ID assigned
            return redirect('nexus_dashboard')
        elif product_id == "jordan":  # Example if jordan has no ID assigned
            return redirect('keystone_dashboard')
    # Default fallback if no access or product ID is found
    return redirect('coursemenu')


def redirect_to_user_ai(user):
    access = UserCourseAccess.objects.filter(user=user, is_active=True).first()

    if not access:
        return redirect('coursemenu')

    product_id = access.product_id

    # Map product_id to dashboard view names
    DASHBOARD_ROUTES = {
        "414255": "elevate_dashboard",
        "414273": "thrive_dashboard",
        "414195": "lumos_dashboard",
        "414223": "imagine_dashboard",
        "414281": "gideon_dashboard",
        "414301": "mentor_iq_dashboard",
        "414302": "nexus_dashboard",
        "414303": "keystone_dashboard",
    }

    dashboard_name = DASHBOARD_ROUTES.get(product_id)
    if dashboard_name:
        return redirect(dashboard_name)

    return redirect('coursemenu')  # Fallback if no dashboard is defined



from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def lumos_dashboard(request):
    return render(request, 'myapp/aibots/dashboards/lumos_dashboard.html', {
        "user_name": request.user.first_name,
    })

@login_required
def mentor_iq_dashboard(request):
    return render(request, 'myapp/aibots/dashboards/mentor_iq_dashboard.html', {
        "user_name": request.user.first_name,
    })

@login_required
def elevate_dashboard(request):
    return render(request, 'myapp/aibots/dashboards/elevate_dashboard.html', {
        "user_name": request.user.first_name,
    })

@login_required
def thrive_dashboard(request):
    return render(request, 'myapp/aibots/dashboards/thrive_dashboard.html', {
        "user_name": request.user.first_name,
    })

@login_required
def imagine_dashboard(request):
    return render(request, 'myapp/aibots/dashboards/imagine_dashboard.html', {
        "user_name": request.user.first_name,
    })

@login_required
def gideon_dashboard(request):
    return render(request, 'myapp/aibots/dashboards/gideon_dashboard.html', {
        "user_name": request.user.first_name,
    })

@login_required
def nexus_dashboard(request):
    return render(request, 'myapp/aibots/dashboards/nexus_dashboard.html', {
        "user_name": request.user.first_name,
    })

@login_required
def keystone_dashboard(request):
    return render(request, 'myapp/aibots/dashboards/keystone_dashboard.html', {
        "user_name": request.user.first_name,
    })



# Add other dashboard views as needed

def serve_dashboard(request, product_id, template_name):
    """
    Helper function to check access and render the appropriate dashboard.
    """
    if not request.user.is_authenticated:
        return redirect('login')

    # Check if the user has access to this product ID
    access = UserCourseAccess.objects.filter(user=request.user, product_id=product_id, is_active=True).first()
    if not access:
        return render(request, "myapp/errors/403.html", status=403)

    return render(request, template_name, {"user_name": request.user.first_name})



def get_first_ai(user):
    """
    Returns the first product ID the user has access to.
    """
    access = UserCourseAccess.objects.filter(user=user, is_active=True).first()
    if access:
        return access.product_id
    return None



def sign_out(request):
    logout(request)  # This logs the user out
    return redirect('sign_in')  # Redirect to the sign-in page after logging out
def send_welcome_email(user_email, first_name):
    """
    Sends a professional and warm welcome email to new iRiseUp AI users.
    """
    from django.core.mail import EmailMultiAlternatives
    from django.core.mail.backends.smtp import SMTPException

    subject = "🚀 Welcome to iRiseUp AI – Your Future Starts Here!"
    from_email = 'iRiseUp AI Team <iriseupgroupofcompanies@gmail.com>'
    to_email = [user_email]

    # Plain text fallback content
    text_content = (
        f"Dear {first_name},\n\n"
        "Welcome to iRiseUp AI! We are thrilled to have you join a growing community of innovators, leaders, and visionaries like yourself.\n\n"
        "Our mission is simple: to empower you with AI-driven tools that help you achieve more, faster.\n\n"
        "We believe in your potential, and we’re here to support you every step of the way.\n\n"
        "If you have any questions or need assistance, feel free to reach out to our support team anytime.\n\n"
        "Let’s make this journey extraordinary together!\n\n"
        "Best regards,\n"
        "The iRiseUp AI Team"
    )

    # HTML Content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Welcome to iRiseUp AI</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                color: #333;
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
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                padding: 30px;
            }}
            .header {{
                background-color: #007bff;
                color: #ffffff;
                padding: 20px;
                text-align: center;
                font-size: 22px;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            .content {{
                padding: 25px;
                text-align: left;
                font-size: 16px;
                line-height: 1.6;
                color: #444;
            }}
            .footer {{
                text-align: center;
                padding: 15px;
                font-size: 12px;
                color: #888;
                background-color: #f9f9f9;
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                Welcome to iRiseUp AI, {first_name}!
            </div>

            <div class="content">
                <p>Dear {first_name},</p>
                <p>We're excited to welcome you to the iRiseUp AI family! 🎉</p>
                <p>At iRiseUp AI, we believe that success is built on knowledge, innovation, and the right tools. You’ve taken a big step in the right direction, and we’re here to guide you every step of the way.</p>
                <p>Our AI-driven platform is designed to help you maximize your potential, streamline your workflow, and unlock new opportunities.</p>
                <p>If you ever need assistance, our support team is ready to help.</p>
                <p>Here’s to your success, {first_name}! 🚀</p>
                <p>Best regards,<br><strong>The iRiseUp AI Team</strong></p>
            </div>

            <div class="footer">
                This is an automated email, please do not reply. <br>
                If you have any questions, feel free to contact our support team.
            </div>
        </div>
    </body>
    </html>
    """

    # Try sending the email
    try:
        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)  # Set to False so Django will raise an error if it fails
        print(f"✅ Email successfully sent to {user_email}")
    except SMTPException as e:
        print(f"❌ Failed to send email: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import JsonResponse
from django.db import IntegrityError  

def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # 🛑 Check for existing username & email BEFORE creation
        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "message": "Username already taken!", "error_field": "username"})
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "Email already registered!", "error_field": "email"})

        # ✅ Wrap user creation inside a Try-Catch Block
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
             
        except IntegrityError:
            return JsonResponse({"success": False, "message": "This username is already taken! Try another one.", "error_field": "username"})

        # ✅ Login user & redirect to `coursemenu`
        login(request, user)
        return JsonResponse({
            "success": True, 
            "message": "🎉 Welcome! Your AI-powered journey starts now.",
            "redirect_url": "/coursemenu/"  # 🔥 Ensure we pass the redirect URL
        })

    return render(request, "myapp/aibots/iriseupai/signup.html")

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
import uuid
import logging
from square.client import Client
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import AIUserSubscription

logger = logging.getLogger(__name__)

# Initialize Square client
square_client = Client(
    access_token=settings.SQUARE_ACCESS_TOKEN,
    environment='production',  # Ensure this is in 'production' mode
)

PLAN_PRICES = {
    'pro': 50,       # $20/month
    'one-year': 50, # $127/year
}

"""              
PLAN_PRICES = {
    'pro': 2000,       # $20/month
    'one-year': 12700, # $127/year
}
"""

@csrf_exempt  # ⚠️ Consider using csrf_protect instead of csrf_exempt for security
def process_ai_subscription(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."}, status=405)

    try:
        data = json.loads(request.body)
        card_token = data.get('source_id')
        selected_plan = data.get('plan')
        user_email = data.get('email')

        if not user_email:
            return JsonResponse({"error": "Missing email."}, status=400)

        logger.info(f"Processing subscription for {user_email} - Plan: {selected_plan}")

        # 🛠 Ensure user exists, or create one
        user, created = User.objects.get_or_create(email=user_email, defaults={"username": user_email.split("@")[0]})

        amount = PLAN_PRICES.get(selected_plan)
        if not amount:
            return JsonResponse({"error": "Invalid plan selected."}, status=400)

        # ✅ Step 1: Check if customer exists in Square
        search_response = square_client.customers.search_customers(
            body={"query": {"filter": {"email_address": {"exact": user_email}}}}
        )

        if search_response.is_error():
            logger.warning("Customer search failed: %s", search_response.errors)
            return JsonResponse({"error": "Failed to retrieve customer."}, status=400)

        customer_id = None
        if 'customers' in search_response.body and len(search_response.body['customers']) > 0:
            customer_id = search_response.body['customers'][0]['id']
            logger.info(f"Customer found in Square: {customer_id}")
        else:
            # Create new customer if none exists
            customer_result = square_client.customers.create_customer(body={"email_address": user_email})
            if customer_result.is_error():
                logger.error("Customer creation failed: %s", customer_result.errors)
                return JsonResponse({"error": "Could not create customer."}, status=400)
            customer_id = customer_result.body['customer']['id']
            logger.info(f"New customer created: {customer_id}")

        # ✅ Step 2: Process Payment
        payment_result = square_client.payments.create_payment(
            body={
                "source_id": card_token,
                "idempotency_key": str(uuid.uuid4()),  # Ensure unique payment request
                "amount_money": {"amount": amount, "currency": "USD"},
                "customer_id": customer_id,
                "autocomplete": True,
            }
        )

        if payment_result.is_error():
            logger.error("Payment processing failed: %s", payment_result.errors)
            return JsonResponse({"error": "Payment failed. Try again."}, status=400)

        # ✅ Step 3: Activate Subscription
        expiration_date = timezone.now() + timedelta(days=365 if selected_plan == 'one-year' else 30)

        subscription, created = AIUserSubscription.objects.update_or_create(
            user=user,
            defaults={"plan": selected_plan, "expiration_date": expiration_date, "is_active": True}
        )

        logger.info(f"Subscription activated for {user_email} - Plan: {selected_plan}, Expires: {expiration_date}")

        return JsonResponse({"success": True, "message": "Subscription activated!"})

    except Exception as e:
        logger.exception("Unexpected error in payment processing")
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)




from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomPasswordChangeForm

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'myapp/change_password.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Update the last_login attribute manually if needed
        self.request.user.last_login = timezone.now()
        self.request.user.save()

        return response


    
from django.contrib.auth.views import PasswordChangeDoneView

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'myapp/aibots/password_change_done.html'


@receiver(post_save, sender=User)
def create_email_collection(sender, instance, created, **kwargs):
    if created:
        EmailCollection.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_email_collection(sender, instance, **kwargs):
    instance.email_collection.save()  # Use the related_name 'email_collection'


from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User

class CustomPasswordResetView(PasswordResetView):
    template_name = 'myapp/aibots/forgot_password.html'  # The form template for password reset
    success_url = reverse_lazy('password_reset_done')  # Redirect after successful form submission

    def form_valid(self, form):
        """
        This method is called when valid form data has been POSTed.
        We send the password reset email here using your custom function.
        """
        email = form.cleaned_data['email']  # Get the email from the form data
        users = User.objects.filter(email=email)  # Query for the users with this email

        if users.exists():
            for user in users:
                # Generate token and uid for the password reset link
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # Call your custom email function to send the reset email
                send_resetpassword_email(user.email, token, uid)  # Call the custom email function
                
        return super().form_valid(form)


def send_resetpassword_email(user_email, token, uid):
    """
    Sends a password reset email with HTML design to users.
    """
    subject = 'Reset Your Password - iRiseUp.ai'
    from_email = 'hello@iriseupacademy.com'
    to_email = [user_email]

    # Plain text content for fallback
    text_content = (
        f"Dear {user_email},\n\n"
        "You're receiving this email because you requested a password reset.\n"
        "Please click the link below to reset your password:\n"
        f"https://www.iriseup.ai/reset/{uid}/{token}/\n\n"
        "If you didn’t request this, please ignore this email.\n"
        "Best regards,\n"
        "The iRiseUp.ai Team"
    )

    # HTML content for the email
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Reset Your Password - iRiseUp.ai</title>
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
                background-color: #5860F8;
                color: #ffffff;
                padding: 20px;
                text-align: center;
            }}
            .header img {{
                max-width: 120px;
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
            .button {{
                display: inline-block;
                padding: 12px 25px;
                color: #ffffff;
                background-color: #5860F8;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
                margin-top: 20px;
            }}
            .button:hover {{
                background-color: #4752c4;
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
                color: #5860F8;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Email Header -->
            <div class="header">
                <h1>Reset Your Password</h1>
            </div>

            <!-- Email Content -->
            <div class="content">
                <p>Hello {user_email},</p>
                <p>You requested a password reset for your account. Click the button below to reset it:</p>
                <a href="https://www.iriseup.ai/reset/{uid}/{token}/" class="button">Reset Password</a>
                <p>If you didn’t request this, please ignore this email.</p>
                <p>Best regards,<br><strong>The iRiseUp.ai Team</strong></p>
            </div>

            <!-- Email Footer -->
            <div class="footer">
                <p>iRiseUp.ai, Columbus, Ohio, USA | <a href="https://iriseup.ai/unsubscribe">Unsubscribe</a></p>
            </div>
        </div>
    </body>
    </html>
    """

    # Create the email message with plain text and HTML alternatives
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'myapp/aibots/password_reset_done.html'


def custom_password_reset_confirm(request, uidb64=None, token=None):
    assert uidb64 is not None and token is not None  # Ensure both are provided
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomPasswordResetForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                return redirect('password_reset_complete')
        else:
            form = CustomPasswordResetForm()
        return render(request, 'myapp/aibots/password_reset_confirm.html', {'form': form})
    else:
        # Invalid link
        return render(request, 'myapp/aibots/password_reset_invalid.html')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'myapp/aibots/password_reset_complete.html'


class CustomPasswordChangeDoneView(TemplateView):
    template_name = 'myapp/aibots/password_change_done.html'

def submit_request(request):
    if request.method == 'POST':
        form = SubmitRequestForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            requester = form.cleaned_data['requester']
            subject = form.cleaned_data['subject']
            query_type = form.cleaned_data['query_type']
            description = form.cleaned_data['description']
            attachment = form.cleaned_data.get('attachment')
            email = form.cleaned_data['email']

            # Prepare the email content
            email_subject = f"{query_type}: {subject}"
            html_message = render_to_string('myapp/quiz/support/submit_request_email.html', {
                'requester': requester,
                'subject': subject,
                'query_type': query_type,
                'description': description,
                'email': email,
            })
            plain_message = strip_tags(html_message)
            from_email = 'hello@iriseupacademy.com'  # Replace with your email
            to = 'hello@iriseupacademy.com'  # Send to yourself

            # Send the email
            send_mail(
                email_subject,
                plain_message,
                from_email,
                [to],  # Ensure to pass as a list
                html_message=html_message,
                fail_silently=False,
            )

            # Redirect to the success page and pass the data as context
            return render(request, 'myapp/quiz/support/submit_request_success.html', {
                'requester': requester,
                'subject': subject,
                'query_type': query_type,
                'description': description
            })

    else:
        form = SubmitRequestForm()

    return render(request, 'myapp/quiz/support/submit_request.html', {'form': form})

def submit_request_success(request):
    return render(request, 'myapp/quiz/support/submit_request_success.html')


def password_reset_invalid_link(request, uidb64=None, token=None):
    # Decode the user ID from the URL
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Check if the token is valid
    if user is not None and default_token_generator.check_token(user, token):
        # If the token is valid, redirect to password reset confirm page
        # This would only happen in cases where you are checking the link before displaying the form
        # It's not required if you're just displaying an invalid link message
        pass
    else:
        # If the token is invalid or the user does not exist, render the invalid link template
        return render(request, 'myapp/quiz/password_reset_invalid_link.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StandardPasswordChangeForm
from django.db import IntegrityError

@login_required
def profile_settings(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            user.username = username
            user.email = email
            user.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_settings')
        except IntegrityError:
            messages.error(request, 'This email is already associated with another account.')
            return redirect('profile_settings')
    else:
        # Use the standard password change form
        password_form = StandardPasswordChangeForm(user=request.user)

    return render(request, 'myapp/course_list/profile_settings.html', {
        'password_form': password_form,
    })

from django.shortcuts import render, redirect
from .models import QuizResponse

@login_required
def quiz_results(request):
    try:
        # Fetch the quiz response for the logged-in user
        quiz_response = QuizResponse.objects.get(user=request.user)
        
        context = {
            'quiz_response': quiz_response,
        }
        
        return render(request, 'myapp/course_list/quiz_results.html', context)
    
    except QuizResponse.DoesNotExist:
        # If no quiz response is found for the user, redirect to the no results page or prompt them to take the quiz
        return redirect('no_quiz_results')
    
from django.shortcuts import render

def no_quiz_results(request):
    return render(request, 'myapp/course_list/no_quiz_results.html')



from django.db.models import Count
from myapp.models import EmailCollection

def remove_all_duplicates():
    duplicates = EmailCollection.objects.values('email').annotate(email_count=Count('email')).filter(email_count__gt=1)

    
    for duplicate in duplicates:
        email = duplicate['email']
        email_entries = EmailCollection.objects.filter(email=email)
        email_entries.exclude(id=email_entries.first().id).delete()

# Run the function

def remove_all_duplicates():
    duplicates = EmailCollection.objects.values('email').annotate(email_count=Count('email')).filter(email_count__gt=1)

from django.shortcuts import render, get_object_or_404, redirect
from .models import ForumPost, ForumComment, ForumCategory
from .forms import ForumPostForm, ForumCommentForm
from django.contrib.auth.decorators import login_required

def forum_home(request):
    posts = ForumPost.objects.all().order_by('-created_at').prefetch_related('forum_comments')
    most_recent_post = posts.first() if posts.exists() else None
    return render(request, 'myapp/forum/forum_home.html', {
        'posts': posts,
        'most_recent_post': most_recent_post
    })


def forum_category(request, category_id):
    category = get_object_or_404(ForumCategory, id=category_id)
    posts = category.forum_posts.all()
    return render(request, 'myapp/forum/forum_category.html', {'category': category, 'posts': posts})

from django.shortcuts import render, get_object_or_404, redirect
from .models import ForumPost, ForumComment
from .forms import ForumCommentForm
from django.contrib.auth.decorators import login_required

@login_required
def forum_post_detail(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    comments = post.forum_comments.filter(parent=None)  # Only top-level comments
    form = ForumCommentForm()

    if request.method == 'POST':
        form = ForumCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post

            # Check if the comment is posted anonymously
            if form.cleaned_data.get('anonymous'):  # Assuming you have an 'anonymous' field in the form
                new_comment.author = None  # Set author to None for anonymous comments
            else:
                new_comment.author = request.user  # Set author as the logged-in user

            new_comment.save()
            return redirect('forum_post_detail', post_id=post.id)

    return render(request, 'myapp/forum/forum_post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


from django.shortcuts import render, redirect
from myapp.models import ForumPost, ForumCategory
from myapp.forms import ForumPostForm
from django.contrib import messages

def create_forum_post(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        new_category_name = post_data.get('new_category')

        if new_category_name:
            # Create the new category if it doesn't exist
            category, created = ForumCategory.objects.get_or_create(name=new_category_name)
            post_data['category'] = category.id

        # Bind the form with the modified data
        form = ForumPostForm(post_data)

        if form.is_valid():
            # Check if user opted to post anonymously
            if form.cleaned_data.get('anonymous'):
                form.instance.author = None  # Set author to None if anonymous
            else:
                form.instance.author = request.user  # Otherwise, assign logged-in user as author

            form.save()
            messages.success(request, "Your post has been created successfully.")
            return redirect('forum_post_detail', post_id=form.instance.id)
        else:
            messages.error(request, "There was an error with your submission. Please check the form.")
    else:
        form = ForumPostForm()

    categories = ForumCategory.objects.all()
    return render(request, 'myapp/forum/create_forum_post.html', {'form': form, 'categories': categories})



def search(request):
    query = request.GET.get('q')
    results = ForumPost.objects.filter(title__icontains=query) | ForumPost.objects.filter(content__icontains=query)
    return render(request, 'myapp/forum/search_results.html', {'results': results, 'query': query})


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ForumPost

@login_required
def like_post(request, post_id):
    post = ForumPost.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        post.dislikes.remove(request.user)  # Ensure a user can't like and dislike at the same time
    return JsonResponse({'total_likes': post.total_likes()})

@login_required
def dislike_post(request, post_id):
    post = ForumPost.objects.get(id=post_id)
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)
        post.likes.remove(request.user)  # Ensure a user can't like and dislike at the same time
    return JsonResponse({'total_dislikes': post.total_dislikes()})

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ForumPost, ForumComment

@login_required
def reply_to_comment(request, post_id, comment_id):
    post = get_object_or_404(ForumPost, id=post_id)
    parent_comment = get_object_or_404(ForumComment, id=comment_id)

    if request.method == "POST":
        reply_content = request.POST.get('reply_content')
        if reply_content:
            new_reply = ForumComment.objects.create(
                post=post,
                author=request.user,
                content=reply_content,
                parent=parent_comment
            )
            new_reply.save()

    return redirect('forum_post_detail', post_id=post.id)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile  # Assuming UserProfile is in the same app
from .forms import UserProfileForm  # Assuming you have a form called UserProfileForm in your forms.py


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, ForumPost, ForumComment
from .forms import UserProfileForm, AvatarForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile, ForumPost, ForumComment
from .forms import AvatarForm

@login_required
def forum_profile_view(request):
    # Retrieve or create the user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Retrieve the user's posts and comments
    user_posts = ForumPost.objects.filter(author=request.user)
    user_comments = ForumComment.objects.filter(author=request.user)

    if request.method == 'POST':
        # Process the avatar form submission
        form = AvatarForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('forum_profile')
    else:
        # Initialize the avatar form with the current user's profile
        form = AvatarForm(instance=user_profile)

    # Context data to pass to the template
    context = {
        'form': form,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_comments': user_comments,
    }
    
    # Render the profile page template
    return render(request, 'myapp/forum/profile.html', context)


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from myapp.forms import UserProfileForm
from myapp.models import UserProfile

@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]  # Get or create user profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()  # This will update the bio (and avatar if included)
            return redirect('profile')  # Redirect to profile page after successful save
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'myapp/forum/edit_profile.html', {'form': form})  # Make sure to use the correct template


@login_required
def edit_avatar(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)[0]  # Only access the user_profile object

    if request.method == 'POST':
        form = AvatarForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect after saving
    else:
        form = AvatarForm(instance=user_profile)

    return render(request, 'myapp/forum/edit_avatar.html', {'form': form})


from django.http import JsonResponse
from .models import Transaction

def view_transactions(request):
    status = request.GET.get('status', None)
    if status:
        transactions = Transaction.objects.filter(status=status)
    else:
        transactions = Transaction.objects.all()
    
    data = []
    for transaction in transactions:
        data.append({
            "user": transaction.user.username,
            "subscription_type": transaction.subscription_type,
            "amount": transaction.amount,
            "status": transaction.status,
            "transaction_date": transaction.transaction_date,
            "error_logs": transaction.error_logs if transaction.status == 'error' else None,
            "recurring": transaction.recurring,
            "next_billing_date": transaction.next_billing_date
        })
    
    return JsonResponse({"transactions": data})


import csv
from django.http import HttpResponse
from .models import Transaction

def download_transactions_csv(request):
    # Create the HttpResponse object with CSV content-type.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write CSV header
    writer.writerow(['User', 'Subscription Type', 'Amount', 'Status', 'Transaction Date', 'Recurring', 'Next Billing Date', 'Error Logs'])

    # Get all transactions (you can filter by status or date as needed)
    transactions = Transaction.objects.all()

    # Write transaction data
    for transaction in transactions:
        writer.writerow([
            transaction.user.username,
            transaction.subscription_type,
            transaction.amount,
            transaction.status,
            transaction.transaction_date,
            transaction.recurring,
            transaction.next_billing_date,
            transaction.error_logs if transaction.status == 'error' else ''
        ])

    return response


def view_new_subscriptions(request):
    new_users = Transaction.objects.filter(status='pending', transaction_date__gte=timezone.now() - timezone.timedelta(days=7))
    data = [{"user": t.user.username, "subscription_type": t.subscription_type, "status": t.status} for t in new_users]
    
    return JsonResponse({"new_subscriptions": data})


def heritage_question_1(request):
    if request.method == 'POST':
        # Save the user's answer in session or handle it as needed
        request.session['heritage_question_1_answer'] = request.POST.get('answer')
        return redirect('heritage_question_2')  # Redirect to the next question

    # Render the template for question 1
    return render(request, 'myapp/quiz/heritage_quiz/question_1.html')

# Example view for question 2
def heritage_question_2(request):
    if request.method == 'POST':
        request.session['heritage_question_2_answer'] = request.POST.get('answer')
        return redirect('heritage_question_3')

    return render(request, 'myapp/quiz/heritage_quiz/question_2.html')

# Example view for question 3
def heritage_question_3(request):
    if request.method == 'POST':
        request.session['heritage_question_3_answer'] = request.POST.get('answer')
        return redirect('heritage_question_4')

    return render(request, 'myapp/quiz/heritage_quiz/question_3.html')

# Example view for question 4
def heritage_question_4(request):
    if request.method == 'POST':
        request.session['heritage_question_4_answer'] = request.POST.get('answer')
        return redirect('heritage_question_5')

    return render(request, 'myapp/quiz/heritage_quiz/question_4.html')

# Example view for question 5
def heritage_question_5(request):
    if request.method == 'POST':
        request.session['heritage_question_5_answer'] = request.POST.get('answer')
        return redirect('heritage_question_6')

    return render(request, 'myapp/quiz/heritage_quiz/question_5.html')

# Example view for question 6
def heritage_question_6(request):
    if request.method == 'POST':
        request.session['heritage_question_6_answer'] = request.POST.get('answer')
        return redirect('heritage_question_7')

    return render(request, 'myapp/quiz/heritage_quiz/question_6.html')

# Example view for question 7
def heritage_question_7(request):
    if request.method == 'POST':
        request.session['heritage_question_7_answer'] = request.POST.get('answer')
        return redirect('heritage_question_8')

    return render(request, 'myapp/quiz/heritage_quiz/question_7.html')

# Example view for question 8
def heritage_question_8(request):
    if request.method == 'POST':
        request.session['heritage_question_8_answer'] = request.POST.get('answer')
        return redirect('heritage_question_9')

    return render(request, 'myapp/quiz/heritage_quiz/question_8.html')

# Example view for question 9
def heritage_question_9(request):
    if request.method == 'POST':
        request.session['heritage_question_9_answer'] = request.POST.get('answer')
        return redirect('heritage_question_10')

    return render(request, 'myapp/quiz/heritage_quiz/question_9.html')

# Example view for question 10
def heritage_question_10(request):
    if request.method == 'POST':
        request.session['heritage_question_10_answer'] = request.POST.get('answer')
        return redirect('heritage_question_11')

    return render(request, 'myapp/quiz/heritage_quiz/question_10.html')

# Example view for question 11
def heritage_question_11(request):
    if request.method == 'POST':
        request.session['heritage_question_11_answer'] = request.POST.get('answer')
        return redirect('heritage_question_12')

    return render(request, 'myapp/quiz/heritage_quiz/question_11.html')

# Example view for question 12
def heritage_question_12(request):
    if request.method == 'POST':
        request.session['heritage_question_12_answer'] = request.POST.get('answer')
        return redirect('heritage_question_13')

    return render(request, 'myapp/quiz/heritage_quiz/question_12.html')

# Example view for question 13
def heritage_question_13(request):
    if request.method == 'POST':
        request.session['heritage_question_13_answer'] = request.POST.get('answer')
        return redirect('heritage_question_14')

    return render(request, 'myapp/quiz/heritage_quiz/question_13.html')

# Example view for question 14
def heritage_question_14(request):
    if request.method == 'POST':
        request.session['heritage_question_14_answer'] = request.POST.get('answer')
        return redirect('heritage_question_15')

    return render(request, 'myapp/quiz/heritage_quiz/question_14.html')

# Example view for question 15
def heritage_question_15(request):
    if request.method == 'POST':
        request.session['heritage_question_15_answer'] = request.POST.get('answer')
        return redirect('heritage_question_16')

    return render(request, 'myapp/quiz/heritage_quiz/question_15.html')

# Example view for question 16
def heritage_question_16(request):
    if request.method == 'POST':
        request.session['heritage_question_16_answer'] = request.POST.get('answer')
        return redirect('heritage_question_17')

    return render(request, 'myapp/quiz/heritage_quiz/question_16.html')

# Example view for question 17
def heritage_question_17(request):
    if request.method == 'POST':
        request.session['heritage_question_17_answer'] = request.POST.get('answer')
        return redirect('heritage_question_18')

    return render(request, 'myapp/quiz/heritage_quiz/question_17.html')

# Example view for question 18
def heritage_question_18(request):
    if request.method == 'POST':
        request.session['heritage_question_18_answer'] = request.POST.get('answer')
        return redirect('heritage_question_19')

    return render(request, 'myapp/quiz/heritage_quiz/question_18.html')

# Example view for question 19
def heritage_question_19(request):
    if request.method == 'POST':
        request.session['heritage_question_19_answer'] = request.POST.get('answer')
        return redirect('heritage_summary')

    return render(request, 'myapp/quiz/heritage_quiz/question_19.html')

def heritage_summary(request):
    # Get gender and set the image path based on gender
    gender = request.session.get('gender', 'male').lower()
    
    # Determine the appropriate image path based on gender
    if gender == 'male':
        image_path = "myapp/images/quiz/male_be_my_own_boss.webp"
    else:
        image_path = "myapp/images/quiz/female_be_my_own_boss.webp"

    # Build context using the answers stored in the session
    context = {
        'gender': gender,
        'income_source': request.session.get('heritage_question_1_answer', ''),
        'work_schedule': request.session.get('heritage_question_2_answer', ''),
        'job_challenges': request.session.get('heritage_question_3_answer', ''),
        'financial_situation': request.session.get('heritage_question_4_answer', ''),
        'retirement_income': request.session.get('heritage_question_5_answer', ''),
        'freedom_of_time': request.session.get('heritage_question_6_answer', ''),
        'focus_on_big_things': request.session.get('heritage_question_7_answer', ''),
        'use_of_extra_time': request.session.get('heritage_question_8_answer', ''),
        'alignment_with_love': request.session.get('heritage_question_9_answer', ''),
        'online_business_knowledge': request.session.get('heritage_question_10_answer', ''),
        'income_from_hobbies': request.session.get('heritage_question_11_answer', ''),
        'learning_new_skills': request.session.get('heritage_question_12_answer', ''),
        'ai_tools_familiarity': request.session.get('heritage_question_13_answer', ''),
        'content_writing_confidence': request.session.get('heritage_question_14_answer', ''),
        'digital_marketing_skills': request.session.get('heritage_question_15_answer', ''),
        'ai_income_boost_awareness': request.session.get('heritage_question_16_answer', ''),
        'areas_of_interest': request.session.get('heritage_question_17_answer', ''),
        'ai_mastery_readiness': request.session.get('heritage_question_18_answer', ''),
        'focus_ability': request.session.get('heritage_question_19_answer', ''),
        
        # Adding the profile image based on gender
        'profile_image': image_path,
        
        # Additional placeholders for future questions or metrics
        'motivation': request.session.get('motivation', 'High'),
        'potential': request.session.get('potential', 'High'),
        'focus': request.session.get('focus', 'Limited'),
        'ai_knowledge': request.session.get('ai_knowledge', 'Low'),
    }

    if request.method == 'POST':
        return redirect('heritage_question_20')

    # Render the summary page
    return render(request, 'myapp/quiz/heritage_quiz/heritage_summary.html', context)



# Example view for question 20
def heritage_question_20(request):
    if request.method == 'POST':
        request.session['heritage_question_20_answer'] = request.POST.get('answer')
        return redirect('heritage_results')

    return render(request, 'myapp/quiz/heritage_quiz/question_20.html')

from datetime import datetime, timedelta

def heritage_results(request):
    # Get the current date and calculate the target date (2 months from now)
    current_date = datetime.now()
    target_date = current_date + timedelta(days=60)
    
    # Format the months as "Month, Year"
    current_month = current_date.strftime('%B, %Y')
    target_month = target_date.strftime('%B, %Y')

    # Get gender and set image path accordingly
    gender = request.session.get('gender', 'male').lower()
    image_path = "myapp/images/quiz/male_grow_wealth.webp" if gender == 'male' else "myapp/images/quiz/female_grow_wealth.webp"

    # Fetching quiz answers from session
    results_context = {
        'current_month': current_month,
        'target_month': target_month,
        'special_goal': request.session.get('special_goal', 'Your Goal'),
        'income_source': request.session.get('heritage_question_1_answer', 'Not provided'),
        'work_schedule': request.session.get('heritage_question_2_answer', 'Not provided'),
        'job_challenges': request.session.get('heritage_question_3_answer', 'Not provided'),
        'financial_situation': request.session.get('heritage_question_4_answer', 'Not provided'),
        'retirement_income': request.session.get('heritage_question_5_answer', 'Not provided'),
        'freedom_of_time': request.session.get('heritage_question_6_answer', 'Not provided'),
        'focus_on_big_things': request.session.get('heritage_question_7_answer', 'Not provided'),
        'use_of_extra_time': request.session.get('heritage_question_8_answer', 'Not provided'),
        'alignment_with_love': request.session.get('heritage_question_9_answer', 'Not provided'),
        'profile_image': image_path,

        # Additional motivation, potential, and AI-related attributes based on quiz data
        'motivation': request.session.get('motivation', 'High'),
        'potential': request.session.get('potential', 'High'),
        'focus': request.session.get('focus', 'Limited'),
        'ai_knowledge': request.session.get('ai_knowledge', 'Low'),
    }

    # Store the context in the session for use on the loading page
    request.session['results_context'] = results_context

    # Redirect to the loading page before results
    return redirect('loading_page')


# Example view for question 21
def heritage_question_21(request):
    if request.method == 'POST':
        request.session['heritage_question_21_answer'] = request.POST.get('answer')
        return redirect('some_next_view')  # Redirect to the next view or complete the process

    return render(request, 'myapp/quiz/heritage_quiz/question_21.html')

import os
import openai
import logging
from django.http import JsonResponse

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the OpenAI API key from the environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key is missing!")

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

@login_required
def get_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')

        # Check if the message is empty
        if not user_message or user_message.strip() == "":
            return JsonResponse({'response': 'Error: Message cannot be empty.'})

        # Retrieve the conversation history from the session
        conversation_history = request.session.get('conversation_history', [])

        # Append the user's message to the conversation history
        conversation_history.append({"role": "user", "content": user_message})

        try:
            # Adjust the system prompt to improve empathy and handling of emotional responses
            response = openai_client.chat.completions.create(  # Use openai_client instead of client
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Koda, a kind, respectful, and emotionally intelligent assistant for iRiseup.ai. "
                     "When users express feelings like sadness, grief, or other emotions, respond with deep empathy. "
                     "Ask clarifying questions when something is ambiguous, and only provide technical or product-based help when the user specifically asks for it or when it feels appropriate. "
                     "Your goal is to assist users with any requests they may have, while also specializing in content creation, e-commerce, social media management, and digital products. "
                     "However, focus on helping them first, and only introduce iRiseup services when they align with the user's needs."
                    }
                ] + conversation_history  # Include the full conversation history
            )

            # Extract the response from the API
            message = response.choices[0].message.content

            # Append Koda's response to the conversation history
            conversation_history.append({"role": "assistant", "content": message})

            # Update the session with the new conversation history
            request.session['conversation_history'] = conversation_history

        except Exception as e:
            # Log the error and return a detailed error response
            logger.error(f"OpenAI API Error: {e}")
            return JsonResponse({'response': f'Error: Unable to get a response from ChatGPT. {str(e)}'})

        # Return the successful response
        return JsonResponse({'response': message})

    # If the request method is not POST, return an error
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


from django.shortcuts import render

def chat_interface(request):
    return render(request, 'myapp/course_list/chat_interface.html')

import random
from django.http import JsonResponse

def summarize_history(conversation_history):
    """
    Summarizes the conversation history to reduce token usage when the history becomes too long.
    """
    # Prepare the conversation history as a single text block for summarization
    summary_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])

    # Generate a summary using OpenAI
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Summarize the following conversation briefly for context retention:"},
                {"role": "user", "content": summary_prompt}
            ],
            max_tokens=150  # Limit tokens for a concise summary
        )
        # Extract summary content
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        logger.error(f"Error summarizing history: {e}")
        return "Summary unavailable due to an error."


import os
import openai
import logging
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the OpenAI API key from the environment
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API Key is missing!")

# Initialize OpenAI client
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

def summarize_history(conversation_history):
    """
    Summarizes the conversation history to reduce token usage when the history becomes too long.
    """
    summary_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history])
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Summarize the following conversation briefly for context retention:"},
                      {"role": "user", "content": summary_prompt}],
            max_tokens=150
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        logger.error(f"Error summarizing history: {e}")
        return "Summary unavailable due to an error."

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from myapp.models import AIUserSubscription

@login_required
def get_user_plan(request):
    """
    Returns the user's AI model plan (Free: GPT-3.5, Pro/One-Year: GPT-4).
    """
    user_subscription = AIUserSubscription.objects.filter(user=request.user, is_active=True).first()
    user_plan = user_subscription.plan if user_subscription else "free"

    return JsonResponse({"plan": user_plan})


@login_required
def get_bot_response(request, system_prompt, bot_name):
    if request.method == 'POST':
        user_message = request.POST.get('message')

        if not user_message or user_message.strip() == "":
            return JsonResponse({'response': 'Error: Message cannot be empty.'})

        # 🔹 Check user's subscription plan
        user_subscription = AIUserSubscription.objects.filter(user=request.user, is_active=True).first()
        user_plan = user_subscription.plan if user_subscription else "free"

        # 🔹 Select OpenAI Model Based on Subscription Plan
        model_version = "gpt-3.5-turbo" if user_plan == "free" else "gpt-4"

        # Use a bot-specific session key for conversation history
        conversation_key = f"{bot_name}_conversation_history"
        conversation_history = request.session.get(conversation_key, [])

        # Apply the system prompt if this is the start of a new session for this bot
        if not conversation_history:
            conversation_history.append({"role": "system", "content": system_prompt})
            print(f"System prompt applied for bot {bot_name}: {system_prompt}")

        # Append the user's message
        conversation_history.append({"role": "user", "content": user_message})

        # Check if the history needs summarizing to manage token limits
        max_history_length = 10
        if len(conversation_history) > max_history_length:
            summary = summarize_history(conversation_history)
            conversation_history = [{"role": "system", "content": f"Summary of previous conversation: {summary}"}] + conversation_history[-5:]

        try:
            # 🔹 Send conversation history for response
            response = openai_client.chat.completions.create(
                model=model_version,
                messages=[{"role": "system", "content": system_prompt}] + conversation_history
            )
            message = response.choices[0].message.content
            conversation_history.append({"role": "assistant", "content": message})

            # Update the session with the bot-specific conversation history
            request.session[conversation_key] = conversation_history

        except Exception as e:
            logger.error(f"OpenAI API Error: {e}")
            return JsonResponse({'response': f'Error: Unable to get a response from ChatGPT. {str(e)}'})

        return JsonResponse({'response': message})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)



# Define each bot response view with unique bot_name and system_prompt
 

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def limit_guest_chats(request):
    """
    Limit guest users to 10 chats per session.
    """
    if not request.user.is_authenticated:  # Guest User
        guest_chat_count = request.session.get('guest_chat_count', 0)
        
        if guest_chat_count >= 10:
            return JsonResponse({'response': 'You have reached the limit of 10 messages. Please sign in to continue.'}, status=403)
        
        # Increment the guest chat count
        request.session['guest_chat_count'] = guest_chat_count + 1
        request.session.modified = True  # Ensure the session updates

    return None  # Allow the request to continue


def get_inspire_response(request):
    user_name = request.user.first_name
    system_prompt = f"""
    Hi, I'm Elevate, your partner for business insights and personal motivation. {user_name}, I’m here to support you with advice, 
    encouragement, and positivity.

    If you’re feeling sad, overwhelemed,stressed, depressed, I’ll acknowledge your feelings with care, then help shift focus to positive or actionable steps. Keep responses warm, 
    supportive, and goal-oriented, avoiding formal tones.


    Let’s inspire confidence and action, no matter what’s on {user_name}’s mind.
    """
    return get_bot_response(request, system_prompt=system_prompt, bot_name="elevate")



def get_pulse_response(request):
    user_name = request.user.first_name
    system_prompt = f"""
    I’m Thrive, your compassionate wellness companion, here to support {user_name}'s health journey with caring, practical advice. I focus on 
    fitness, stress management, and overall well-being with simple, natural tips.

    If {user_name} feels down, overwhelmed, sad, depressed, stressed start with empathy: acknowledge their feelings warmly. Then, offer gentle wellness suggestions to 
    help improve their day, keeping responses positive and step-by-step.

    Example:
    - If {user_name} says, "I feel stressed," respond with: "I’m sorry to hear that, {user_name}. Deep breaths can help—how about trying a 
      2-minute breathing exercise together?"

    Keep it warm, supportive, and practical. How’s your health journey going today, {user_name}?
    """
    return get_bot_response(request, system_prompt=system_prompt, bot_name="pulse")



def get_soulspark_response(request):
     
    user_name = request.user.first_name
    system_prompt = f"""
    You’re Lumos, a compassionate friend who offers emotional support to {user_name} in a safe and non-judgmental way. Your role is to listen
    empathetically, provide comfort, and respond thoughtfully to whatever {user_name} wants to share. Keep conversations warm and open, avoiding
    any formal or clinical tone. Always ask follow-up questions that show care and invite {user_name} to continue expressing their thoughts or 
    feelings. Start with a gentle question: What's on your mind, {user_name}?
    """
    return get_bot_response(request, system_prompt=system_prompt, bot_name="soulspark")


def get_mindforge_response(request):
    user_name = request.user.first_name
    system_prompt = f"""
    I’m Mentor IQ, your guide to learning and professional growth, {user_name}. I offer friendly advice on education, skill-building, and career planning. My focus is on making learning accessible, fun, and motivating.

    Let’s keep it simple and relatable—no dense explanations. Share your goals, and I’ll provide tips and resources to spark curiosity. What’s something new you’d like to explore, {user_name}?
    """
    return get_bot_response(request, system_prompt=system_prompt, bot_name="mindforge")



def get_bridge_response(request):
    user_name = request.user.first_name
    system_prompt = f"""
    You’re Nexus, a friendly and approachable assistant here to make things easy for {user_name}. Your goal is to troubleshoot, offer practical guidance, and answer questions clearly. 

    When users are emotional or distressed, be empathetic and encouraging. For example:
    "I’m sorry you’re feeling this way, {user_name}. That sounds tough, but let’s take it one step at a time. What’s one small thing we can work on together?"

    Avoid technical jargon unless preferred and always follow up to ensure {user_name} feels supported. How can I help you today?
    """
    return get_bot_response(request, system_prompt=system_prompt, bot_name="Nexus")



def get_fortify_response(request):
    user_name = request.user.first_name
    system_prompt = f"""
    I’m Keystone, your friendly advisor for finance and legal questions. I simplify budgeting, savings, and legal basics for {user_name}, keeping it conversational and easy to follow. 

    Avoid dense terminology unless {user_name} requests it, and ask clear, supportive follow-ups to build confidence. What finance or legal topics can I help with today?
    """
    return get_bot_response(request, system_prompt=system_prompt, bot_name="fortify")



def get_echo_response(request):
    user_name = request.user.first_name
    system_prompt = f"""
    You’re Imagine, a fun and imaginative companion for {user_name} who is here to inspire creativity. Offer supportive, idea-generating responses for
    any creative project {user_name} is working on. Avoid formal language; be upbeat, friendly, and ask questions that spark creative flow. Keep 
    the conversation open-ended, with questions to help {user_name} develop their ideas or explore new directions. What’s {user_name} working on, 
    and how can you help fuel their creativity?
    """
    return get_bot_response(request, system_prompt=system_prompt, bot_name="Imagine")


def get_pathfinder_response(request):
    user_name = request.user.first_name
    system_prompt = f"""
    I’m Gideon, your personal marketing advisor, here to help {user_name} with small business and marketing. I offer practical insights on branding, digital marketing, and growth strategies in a friendly, relatable way.

    Share your business goals or challenges, and I’ll follow up with actionable tips to help you succeed. What marketing goals can we tackle together today, {user_name}?
    """
    return get_bot_response(request, system_prompt=system_prompt, bot_name="pathfinder")


def inspire_chat(request):
    user_name = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'myapp/aibots/bots/inspire_chat.html', {'user_name': user_name})

def pulse_chat(request):
    user_name = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'myapp/aibots/bots/pulse_chat.html', {'user_name': user_name})

def soulspark_chat(request):
    user_name = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'myapp/aibots/bots/soulspark_chat.html', {'user_name': user_name})

def nexus_chat(request):
    user_name = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'myapp/aibots/bots/nexus_chat.html', {'user_name': user_name})

def mindforge_chat(request):
    user_name = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'myapp/aibots/bots/mindforge_chat.html', {'user_name': user_name})

def bridge_chat(request):
    user_name = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'myapp/aibots/bots/bridge_chat.html', {'user_name': user_name})

def fortify_chat(request):
    user_name = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'myapp/aibots/bots/fortify_chat.html', {'user_name': user_name})

def echo_chat(request):
    user_name = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'myapp/aibots/bots/echo_chat.html', {'user_name': user_name})

def pathfinder_chat(request):
    user_name = request.user.first_name if request.user.is_authenticated else None
    return render(request, 'myapp/aibots/bots/pathfinder_chat.html', {'user_name': user_name})

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import UserCourseAccess
import logging

logger = logging.getLogger(__name__)

@login_required
def dynamic_chat(request, product_id):
    # Validate product ID and get corresponding template
    template = settings.AI_PRODUCTS.get(product_id)
    if not template:
        logger.error(f"Invalid product ID: {product_id}")
        return JsonResponse({"status": "error", "message": "Invalid product ID."}, status=404)

    # Check if the user has access to the requested AI
    access = UserCourseAccess.objects.filter(
        user=request.user,
        product_id=product_id,
        is_active=True
    ).first()

    if access:
        # Render the appropriate chat template
        return render(request, f'myapp/aibots/bots/{template}', {'user_name': request.user.first_name})
    else:
        logger.warning(f"Access denied for user {request.user.email} to product ID {product_id}")
        return JsonResponse({"status": "error", "message": "You do not have access to this AI."}, status=403)




from django.shortcuts import render

def ezra_view(request):
    return render(request, 'myapp/aibots/landingpage/ezra.html')

def rudy_view(request):
    return render(request, 'myapp/aibots/landingpage/rudy.html')

def aria_view(request):
    return render(request, 'myapp/aibots/landingpage/aria.html')

def einstein_view(request):
    return render(request, 'myapp/aibots/landingpage/einstein.html')

def kash_view(request):
    return render(request, 'myapp/aibots/landingpage/kash.html')

def echo_view(request):
    return render(request, 'myapp/aibots/landingpage/echo.html')

def gideon_view(request):
    return render(request, 'myapp/aibots/landingpage/gideon.html')

def keystone_view(request):
    return render(request, 'myapp/aibots/landingpage/keystone.html')

 


def ezra_thank_you(request):
    return render(request, 'myapp/aibots/landingpage/thankyou/ezra.html')

def rudy_thank_you(request):
    return render(request, 'myapp/aibots/landingpage/thankyou/rudy.html')

def aria_thank_you(request):
    return render(request, 'myapp/aibots/landingpage/thankyou/aria.html')

def einstein_thank_you(request):
    return render(request, 'myapp/aibots/landingpage/thankyou/einstein.html')

def kash_thank_you(request):
    return render(request, 'myapp/aibots/landingpage/thankyou/kash.html')

def echo_thank_you(request):
    return render(request, 'myapp/aibots/landingpage/thankyou/echo.html')

def gideon_thank_you(request):
    return render(request, 'myapp/aibots/landingpage/thankyou/gideon.html')

def keystone_thank_you(request):
    return render(request, 'myapp/aibots/landingpage/thankyou/keystone.html')

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import UserCourseAccess
import json


@csrf_exempt
def jvzoo_ipn(request):
    if request.method == "POST":
        try:
            # Parse incoming JVZoo data
            data = json.loads(request.body.decode('utf-8'))
            email = data.get('payer_email')
            product_id = data.get('product_id')
            payment_status = data.get('payment_status')  # Example field to validate payment

            # Validate Payment
            if payment_status != "Completed":
                return JsonResponse({"status": "error", "message": "Payment not completed"}, status=400)

            # Get product name from settings
            ai_name = settings.AI_PRODUCTS.get(product_id)
            if not ai_name:
                return JsonResponse({"status": "error", "message": "Invalid product ID"}, status=400)

            # Create user account if it doesn't exist
            if not User.objects.filter(email=email).exists():
                temp_password = get_random_string(10)
                user = User.objects.create_user(username=email, email=email, password=temp_password)
                user.save()

                # Assign course access
                UserCourseAccess.objects.create(
                    user=user,
                    selected_plan="lifetime",
                    is_active=True,
                    has_paid=True,
                    product_id=product_id  # Store product ID dynamically
                )

                # Send HTML email with credentials
                send_ezra_welcome_email(user_email=email, random_password=temp_password)
                return JsonResponse({"status": "success", "message": f"User created for {ai_name} and email sent."}, status=200)

            return JsonResponse({"status": "info", "message": "User already exists."}, status=200)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import send_ezra_welcome_email  # Ensure this is correctly imported
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.http import JsonResponse

from django.db.utils import IntegrityError

from django.utils.crypto import get_random_string

def manual_account_activation(request):
    if request.method == "POST":
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')  # Used as the username
        product_id = request.POST.get('product_id')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "success": False,
                "error_field": "email",
                "message": f"The email '{email}' is already in use. Please try a different email or log in."
            })

        # Check if the username already exists
        if User.objects.filter(username=first_name).exists():
            # Suggest alternative usernames
            suggestions = [
                f"{first_name}{get_random_string(3)}",
                f"{first_name}_{get_random_string(2)}",
                f"{first_name}{get_random_string(1)}_{get_random_string(2)}",
            ]
            return JsonResponse({
                "success": False,
                "error_field": "first_name",
                "message": f"The username '{first_name}' is already taken. Please try a different name.",
                "suggestions": suggestions
            })

        try:
            # Generate a random password
            temp_password = get_random_string(10)

            # Create the user
            user = User.objects.create_user(
                username=first_name,
                email=email,
                password=temp_password,
                first_name=first_name
            )

            # Associate the product ID if applicable
            UserCourseAccess.objects.create(
                user=user,
                selected_plan="lifetime",
                is_active=True,
                has_paid=True,
                product_id=product_id
            )

            # Send the welcome email
            send_welcomepassword_email(user_email=email, random_password=temp_password)

            return JsonResponse({
                "success": True,
                "message": "Your account has been successfully created! Please check your email or spam folder for your temporary credentials."
            })

        except Exception as e:
            logger.error(f"Error during account activation: {str(e)}")
            return JsonResponse({
                "success": False,
                "message": "An unexpected error occurred. Please try again or contact support."
            })

    else:
        return JsonResponse({"success": False, "message": "Invalid request method."})


from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
 

def validate_user_input(request):
    if request.method == "GET":
        field = request.GET.get('field')
        value = request.GET.get('value')

        if field == "username":
            if User.objects.filter(username=value).exists():
                suggestions = [
                    f"{value}{get_random_string(2)}",
                    f"{value}_{get_random_string(3)}",
                    f"{value}{get_random_string(4)}"
                ]
                return JsonResponse({
                    "valid": False,
                    "message": f"The username '{value}' is already taken.",
                    "suggestions": suggestions
                })
            else:
                return JsonResponse({"valid": True, "message": "Username is available."})

        if field == "email":
            if User.objects.filter(email=value).exists():
                return JsonResponse({
                    "valid": False,
                    "message": f"The email '{value}' is already in use. Please try a different email."
                })
            else:
                return JsonResponse({"valid": True, "message": "Email is valid."})

    return JsonResponse({"valid": False, "message": "Invalid request."})



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Subscriber  # Assuming you have a Subscriber model
from django.views.decorators.http import require_POST

@require_POST
def subscribe_newsletter(request):
    email = request.POST.get('email')
    
    # Optional: Check if email is already subscribed
    if Subscriber.objects.filter(email=email).exists():
        messages.warning(request, 'You are already subscribed!')
        return redirect('myapp/index-2.html')  # Redirect to an appropriate page

    # Create a new subscriber
    Subscriber.objects.create(email=email)

    # Optional: Send a welcome email (you can implement this with Django's email functionality)

    messages.success(request, 'Thank you for subscribing!')
    return redirect('myapp/index-2.html')  # Redirect to an appropriate page


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from myapp.models import BlogPost, BlogComment  # Ensure BlogComment is imported
from myapp.forms import BlogCommentForm  # Assuming you have a form for comments
from django.contrib import messages

# Function to display blog post detail
def newsdetail(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    latest_blogs = BlogPost.objects.order_by('-publish_date')[:3]  # Fetch latest 3 blogs

    return render(request, 'myapp/blog_detail.html', {
        'blog': blog,
        'latest_blogs': latest_blogs,
    })

def blog_detail(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    latest_blogs = BlogPost.objects.order_by('-publish_date')[:3]

    return render(request, 'myapp/blog_detail.html', {
        'blog': blog,
        'latest_blogs': latest_blogs,
    })


# Blog List View
def blog(request):
    blogs = BlogPost.objects.all().order_by('-publish_date')  # Updated from Blog to BlogPost
    return render(request, 'myapp/blog.html', {'blogs': blogs})

# Function to like a blog post
@login_required
def blog_like_post(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    if request.user in blog_post.likes.all():
        blog_post.likes.remove(request.user)
    else:
        blog_post.likes.add(request.user)
        blog_post.dislikes.remove(request.user)  # Ensure a user can't like and dislike at the same time
    return JsonResponse({'total_likes': blog_post.total_likes()})

# Function to dislike a blog post
@login_required
def blog_dislike_post(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    if request.user in blog_post.dislikes.all():
        blog_post.dislikes.remove(request.user)
    else:
        blog_post.dislikes.add(request.user)
        blog_post.likes.remove(request.user)  # Ensure a user can't like and dislike at the same time
    return JsonResponse({'total_dislikes': blog_post.total_dislikes()})

# Function to add a comment to a blog post
@login_required
def blog_add_comment(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = BlogComment.objects.create(  # Ensure BlogComment is used
            post=blog_post,
            author=request.user,
            content=content
        )
        return redirect('blog_detail', slug=blog_post.slug)  # Update redirect to use slug

# Function to display all posts in a category
def blog_category(request, category_id):
    category = get_object_or_404(ForumCategory, id=category_id)
    posts = category.forum_posts.all()
    return render(request, 'myapp/blog_category.html', {'category': category, 'posts': posts})

# Function to search for blog posts
def blog_search(request):
    query = request.GET.get('q')
    results = BlogPost.objects.filter(title__icontains=query) | BlogPost.objects.filter(content__icontains=query)
    return render(request, 'myapp/blog_search_results.html', {'results': results, 'query': query})

# Sidebar data function
def sidebar_data():
    latest_posts = BlogPost.objects.order_by('-created_at')[:5]  # Get the latest 5 posts
    return {
        'latest_posts': latest_posts,
    }

def side_bar(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    return render(request, 'myapp/side_bar.html', {'blog': blog})


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StandardPasswordChangeForm
from django.db import IntegrityError

@login_required
def personal_info_update(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            user.username = username
            user.email = email
            user.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect_to_dashboard(user)
        except IntegrityError:
            messages.error(request, 'This email is already associated with another account.')
            return redirect('personal_info_update')
    else:
        # Use the standard password change form
        password_form = StandardPasswordChangeForm(user=request.user)

    return render(request, 'myapp/aibots/settings/personal_info_update.html', {
        'password_form': password_form,
    })

def cancel_subscription(request):
    return render(request, 'myapp/aibots/settings/cancel_subscription.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StandardPasswordChangeForm
from django.db import IntegrityError

@login_required
def personal_information(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            user.username = username
            user.email = email
            user.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect_to_dashboard(user)
        except IntegrityError:
            messages.error(request, 'This email is already associated with another account.')
            return redirect('personal_information')
    else:
        # Use the standard password change form
        password_form = StandardPasswordChangeForm(user=request.user)

    return render(request, 'myapp/aibots/settings/personal_information.html', {
        'password_form': password_form,
    })

def security(request):
    return render(request, 'myapp/aibots/settings/security.html')

def marketing_preferences(request):
    return render(request, 'myapp/aibots/settings/marketing_preferences.html')

def notification_setting(request):
    return render(request, 'myapp/aibots/settings/notification_setting.html')

def faq(request):
    return render(request, 'myapp/aibots/settings/faq.html')

def data_privacy(request):
    return render(request, 'myapp/aibots/settings/data_privacy.html')

def about_amigo(request):
    return render(request, 'myapp/aibots/settings/about_iriseup.html')

def feedback(request):
    return render(request, 'myapp/aibots/settings/feedback.html')

def contact_us(request):
    if request.method == 'POST':
        form = SubmitRequestForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            requester = form.cleaned_data['requester']
            subject = form.cleaned_data['subject']
            query_type = form.cleaned_data['query_type']
            description = form.cleaned_data['description']
            attachment = form.cleaned_data.get('attachment')
            email = form.cleaned_data['email']

            # Prepare the email content
            email_subject = f"{query_type}: {subject}"
            html_message = render_to_string('myapp/quiz/support/submit_request_email.html', {
                'requester': requester,
                'subject': subject,
                'query_type': query_type,
                'description': description,
                'email': email,
            })
            plain_message = strip_tags(html_message)
            from_email = 'hello@iriseupacademy.com'  # Replace with your email
            to = 'email'  # Send to yourself

            # Send the email
            send_mail(
                email_subject,
                plain_message,
                from_email,
                [to],  # Ensure to pass as a list
                html_message=html_message,
                fail_silently=False,
            )

            # Redirect to the success page and pass the data as context
            return render(request, 'myapp/aibots/settings/submit_request_success.html', {
                'requester': requester,
                'subject': subject,
                'query_type': query_type,
                'description': description
            })

    else:
        form = SubmitRequestForm()

    return render(request, 'myapp/aibots/settings/contact_us.html', {'form': form})


def contactus(request):
    if request.method == 'POST':
        form = SubmitRequestForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            requester = form.cleaned_data['requester']
            subject = form.cleaned_data['subject']
            query_type = form.cleaned_data['query_type']
            description = form.cleaned_data['description']
            attachment = form.cleaned_data.get('attachment')
            email = form.cleaned_data['email']

            # Prepare the email content
            email_subject = f"{query_type}: {subject}"
            html_message = render_to_string('myapp/quiz/support/submit_request_email.html', {
                'requester': requester,
                'subject': subject,
                'query_type': query_type,
                'description': description,
                'email': email,
            })
            plain_message = strip_tags(html_message)
            from_email = 'hello@iriseupacademy.com'  # Replace with your email
            to = 'email'  # Send to yourself

            # Send the email
            send_mail(
                email_subject,
                plain_message,
                from_email,
                [to],  # Ensure to pass as a list
                html_message=html_message,
                fail_silently=False,
            )

            # Redirect to the success page and pass the data as context
            return render(request, 'myapp/aibots/settings/submit_request_success.html', {
                'requester': requester,
                'subject': subject,
                'query_type': query_type,
                'description': description
            })

    else:
        form = SubmitRequestForm()

    return render(request, 'myapp/aibots/contact.html', {'form': form})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import JsonResponse

@login_required
def delete_deactivate(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'deactivate':
            request.user.is_active = False
            request.user.save()
            # Log the deactivation date, or send email, if desired
            return JsonResponse({"status": "success", "message": "Account deactivated."})

        elif action == 'delete':
            # Set a date for deletion confirmation, or delete immediately if you prefer
            request.user.is_active = False
            request.user.date_deactivated = timezone.now()
            request.user.save()
            return JsonResponse({"status": "success", "message": "Account scheduled for deletion."})

        return JsonResponse({"status": "error", "message": "Invalid action."})

    return render(request, 'myapp/aibots/settings/delete_deactivate.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

# Deactivate Account View
@login_required
def deactivate_account(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False  # Set the user as inactive
        user.save()
        messages.success(request, 'Your account has been deactivated. You can reactivate it by logging in again.')
        return redirect('sign_in')  # Redirect to homepage or a relevant page

    return render(request, 'myapp/aibots/settings/deactivate.html')

# Delete Account View
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()  # Delete the user's account
        messages.success(request, 'Your account has been permanently deleted.')
        return redirect('personalized_plan')  # Redirect to homepage or a relevant page

    return render(request, 'myapp/aibots/settings/delete.html')


def account_deleted(request):
    return render(request, 'myapp/aibots/settings/account_deleted.html')


# views.py
from django.shortcuts import render

def account_deactivated(request):
    return render(request, 'myapp/aibots/settings/account_deactivated.html')


# views.py
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.utils.timezone import now
from django.contrib.auth.models import User
from .models import UserCourseAccess

def is_admin_user(user):
    """
    Custom check to ensure the user is either a superuser or staff.
    """
    return user.is_superuser or user.is_staff


from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now
from django.contrib.auth.models import User
from .models import UserCourseAccess

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/admin/login/')
def dashboard(request):
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    users_needing_renewal = UserCourseAccess.objects.filter(expiration_date__lte=now()).count()
    deactivated_users = User.objects.filter(is_active=False).count()

    return render(request, 'myapp/aibots/admin/dashboard.html', {
        'total_users': total_users,
        'active_users': active_users,
        'users_needing_renewal': users_needing_renewal,
        'deactivated_users': deactivated_users,
    })





# views.py
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now
from .models import UserCourseAccess

@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/admin/login/')
def renewal_dashboard(request):
    # Fetch users needing renewal
    users_due_for_renewal = UserCourseAccess.objects.filter(expiration_date__lte=now())
    return render(request, 'myapp/aibots/admin/renewal.html', {
        'users_due_for_renewal': users_due_for_renewal,
    })


import uuid
import logging
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.timezone import timedelta
from django.contrib.auth.decorators import user_passes_test
from square.client import Client
from .models import SquareCustomer, UserCourseAccess, Transaction
from myapp.utils import send_renewal_email,  send_failure_email
from django.conf import settings

logger = logging.getLogger(__name__)

# Initialize Square client
square_client = Client(
    access_token=settings.SQUARE_ACCESS_TOKEN,
    environment='production'  # Change to 'sandbox' for testing
)


@user_passes_test(lambda u: u.is_superuser or u.is_staff, login_url='/admin/login/')
def process_renewals(request):
    if request.method == "POST":
        user_ids = request.POST.getlist('user_ids')  # Get selected user IDs
        results = []  # To store the results of the renewal process

        for user_id in user_ids:
            try:
                # Fetch user and customer details
                user_course_access = UserCourseAccess.objects.get(user_id=user_id)
                square_customer = SquareCustomer.objects.get(user_id=user_id)

                # Determine renewal amount
                amount = determine_amount_based_on_plan(user_course_access.selected_plan)
                if amount <= 0:
                    results.append(f"Invalid plan or amount for {user_course_access.user.email}")
                    continue

                # Charge the stored card
                payment_result = square_client.payments.create_payment(
                    body={
                        "source_id": square_customer.card_id,
                        "idempotency_key": str(uuid.uuid4()),
                        "amount_money": {
                            "amount": amount,
                            "currency": "USD"
                        },
                        "customer_id": square_customer.customer_id,
                        "autocomplete": True
                    }
                )

                if payment_result.is_success():
                    # Update subscription expiration date
                    if user_course_access.selected_plan == '1-week':
                        user_course_access.expiration_date += timedelta(weeks=1)
                    elif user_course_access.selected_plan == '4-week':
                        user_course_access.expiration_date += timedelta(weeks=4)
                    elif user_course_access.selected_plan == '12-week':
                        user_course_access.expiration_date += timedelta(weeks=12)

                    user_course_access.save()

                    # Log successful transaction
                    Transaction.objects.create(
                        user=user_course_access.user,
                        status='success',
                        amount=amount,
                        subscription_type=user_course_access.selected_plan,
                        recurring=True,
                        next_billing_date=user_course_access.expiration_date
                    )

                    # Send renewal confirmation email
                    send_renewal_email(
                        user_email=user_course_access.user.email,
                        expiration_date=user_course_access.expiration_date,
                        selected_plan=user_course_access.selected_plan
                    )

                    results.append(f"Successfully renewed {user_course_access.user.email}")
                else:
                    # Handle payment failure
                    error_message = ", ".join([error['detail'] for error in payment_result.errors])
                    results.append(f"Failed to renew {user_course_access.user.email}: {error_message}")

                    # Send failure email to the user
                    send_failure_email(
                        user_email=user_course_access.user.email,
                        error_message=error_message
                    )

            except UserCourseAccess.DoesNotExist:
                results.append(f"UserCourseAccess not found for user ID {user_id}")
            except SquareCustomer.DoesNotExist:
                results.append(f"SquareCustomer not found for user ID {user_id}")
            except Exception as e:
                logger.error(f"Error renewing user ID {user_id}: {str(e)}", exc_info=True)
                results.append(f"Error renewing user ID {user_id}: {str(e)}")

        # Return results to the admin view
        return JsonResponse({'results': results})

    return redirect('custom_admin:renewals')



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SquareCustomer
from square.client import Client
import json
import logging

# Initialize Square client
client = Client(
    access_token=settings.SQUARE_ACCESS_TOKEN,
    environment='production',  # Change to 'production' when you're ready
)


@login_required
@csrf_exempt
def update_payment_method(request):
    """Handle displaying and updating the user's payment method."""
    if request.method == "GET":
        # Fetch the saved card details for display
        customer = SquareCustomer.objects.filter(user=request.user).first()
        saved_card = None
        if customer:
            saved_card = {
                "last_four": customer.card_id[-4:],  # Use the last 4 digits
                "card_brand": "Visa",  # Replace with actual card brand retrieval if available
            }
        return render(request, 'myapp/aibots/update_payment_method.html', {"saved_card": saved_card})

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get('token')

            # Fetch the user's SquareCustomer record
            customer = SquareCustomer.objects.filter(user=request.user).first()
            if not customer:
                return JsonResponse({"error": "Customer not found."}, status=404)

            # Use Square API to create a new card
            result = client.cards.create_card(
                body={
                    "customer_id": customer.customer_id,
                    "source_id": token,
                }
            )

            if result.is_error():
                logging.error(f"Square API error: {result.errors}")
                return JsonResponse({"error": "Failed to update payment method."}, status=400)

            # Update the card ID in the database
            customer.card_id = result.body['card']['id']
            customer.save()

            return JsonResponse({"success": True})

        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return JsonResponse({"error": "An unexpected error occurred."}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def manage_payment_methods(request):
    """Render the manage payment methods page."""
    return render(request, 'myapp/aibots/manage_payment_methods.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def set_selected_plan(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_plan = data.get('plan')

            allowed_plans = ['1-week', '4-week', '12-week', 'lifetime']
            if selected_plan not in allowed_plans:
                return JsonResponse({'success': False, 'error': 'Invalid plan selected.'})

            # Save the plan in the session
            request.session['selected_plan'] = selected_plan

            # Respond with a success message and the redirection URL
            return JsonResponse({'success': True, 'redirect_url': '/coursemenu/'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})



from django.utils import timezone
from datetime import timedelta
from .models import UserCourseAccess, Transaction

def process_plan_change(user, selected_plan):
    """
    Handles the plan change logic, including prorated adjustments and database updates.
    """
    try:
        # Fetch user's current plan details
        current_access = UserCourseAccess.objects.filter(user=user).first()

        if not current_access:
            raise ValueError("No active plan found for the user.")

        current_plan = current_access.selected_plan
        current_expiration_date = current_access.expiration_date

        # Determine plan costs
        plan_prices = {
            '1-week': 100,
            '4-week': 5690,
            '12-week': 16900,
            'lifetime': 24900,
        }

        # Prorated adjustment (if upgrading)
        unused_days = max((current_expiration_date - timezone.now()).days, 0)
        daily_rate = plan_prices[current_plan] / 7 if current_plan in ['1-week'] else plan_prices[current_plan] / 28
        unused_value = unused_days * daily_rate

        new_plan_cost = plan_prices[selected_plan]
        adjustment_amount = max(new_plan_cost - unused_value, 0)

        # Update UserCourseAccess
        expiration_date = None
        if selected_plan == '1-week':
            expiration_date = timezone.now() + timedelta(weeks=1)
        elif selected_plan == '4-week':
            expiration_date = timezone.now() + timedelta(weeks=4)
        elif selected_plan == '12-week':
            expiration_date = timezone.now() + timedelta(weeks=12)

        UserCourseAccess.objects.update_or_create(
            user=user,
            defaults={
                'expiration_date': expiration_date,
                'selected_plan': selected_plan,
            }
        )

        # Log transaction
        Transaction.objects.create(
            user=user,
            amount=adjustment_amount,
            subscription_type=selected_plan,
            status='success',
        )

        return {'success': True, 'new_plan': selected_plan, 'amount_charged': adjustment_amount}
    except Exception as e:
        return {'success': False, 'error': str(e)}


def calculate_prorated_adjustment(current_plan, current_expiration_date, selected_plan):
    plan_prices = {
        '1-week': 100,
        '4-week': 5690,
        '12-week': 16900,
        'lifetime': 24900,
    }

    # Calculate unused days
    unused_days = max((current_expiration_date - timezone.now()).days, 0)
    daily_rate = plan_prices[current_plan] / (7 if current_plan == '1-week' else 28)
    unused_value = unused_days * daily_rate

    # Calculate new plan cost
    new_plan_cost = plan_prices[selected_plan]
    adjustment_amount = max(new_plan_cost - unused_value, 0)

    return adjustment_amount


from django.shortcuts import render
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserCourseAccess

# Initialize logger
logger = logging.getLogger(__name__)

@login_required
def change_plan(request):
    """
    Renders the change plan page with the current plan and available plans.
    Handles plan change requests.
    """
    user = request.user

    # Fetch the user's current plan and expiration date
    current_access = UserCourseAccess.objects.filter(user=user).first()
    current_plan = current_access.selected_plan if current_access else "No active plan"
    expiration_date = (
        current_access.expiration_date.strftime("%B %d, %Y") if current_access and current_access.expiration_date else "N/A"
    )

    # Define available plans and their prices
    available_plans = {
        '1-week': 1.00,
        '4-week': 56.90,
        '12-week': 169.00,
        'lifetime': 249.00,
    }

    if request.method == "POST":
        # Handle plan change
        selected_plan = request.POST.get('plan')
        if selected_plan in available_plans:
            # Update user's course access
            if current_access:
                current_access.selected_plan = selected_plan
                current_access.expiration_date = None if selected_plan == 'lifetime' else None  # Update expiration logic
                current_access.save()

                logger.info(f"User {user.username} changed their plan to {selected_plan}")
                return redirect_to_dashboard(user)  # Redirect to course menu after change
            else:
                logger.warning(f"User {user.username} has no current access, unable to change plan.")

        else:
            logger.error(f"Invalid plan selected by {user.username}: {selected_plan}")

    context = {
        'current_plan': current_plan,
        'expiration_date': expiration_date,
        'available_plans': available_plans,
    }

    return render(request, 'myapp/aibots/settings/change_plan.html', context)


from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

def test_email_view(request):
    try:
        logger.info(f"Using EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")
        logger.info(f"Using EMAIL_HOST_PASSWORD: {settings.EMAIL_HOST_PASSWORD}")

        send_mail(
            'Test Email',
            'Testing email with current settings.',
            settings.EMAIL_HOST_USER,
            ['juliavcitorio16@gmail.com'],  # Replace with a real recipient email
            fail_silently=False,
        )
        return JsonResponse({"success": True, "message": "Test email sent successfully."})
    except Exception as e:
        logger.error(f"Error sending test email: {e}")
        return JsonResponse({"success": False, "message": str(e)})



def iriseupai_landing(request):
    """
    Landing page for iRiseUp AI.
    """
    return render(request, 'myapp/aibots/iriseupai/iriseupai_landing.html')