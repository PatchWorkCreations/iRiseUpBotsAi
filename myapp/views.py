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

def contact(request):
    return render(request, 'myapp/contact.html')

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

def coursemenu(request):
   

    return render(request, 'myapp/aibots/coursemenu.html')



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
        return 100  # $1.00 in cents
    elif selected_plan == '4-week':
        return 5690  # $56.90 in cents for a 4-week plan (18.97 x 4 with discount)
    elif selected_plan == '12-week':
        return 16900  # $169.00 in cents for a 12-week plan (18.97 x 12 with discount)
    elif selected_plan == 'lifetime':
        return 24900  # $249.00 in cents for the lifetime plan
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
        subject = 'Welcome to iRiseUp Academy!'
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
    subject = 'Welcome to iRiseUp Academy – Your Account is Ready!'
    from_email = 'hello@iriseupacademy.com'
    to_email = [user_email]

    # Plain text content for fallback
    text_content = (
        f"Dear {user_email},\n\n"
        "Welcome to iRiseUp Academy! Your account has been successfully created.\n"
        f"Here is your temporary password: {random_password}\n\n"
        "Please log in to update your password and start your learning journey.\n\n"
        "Best regards,\n"
        "The iRiseUp Academy Team"
    )

    # HTML content (you can use your email design)
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Welcome to iRiseUp Academy</title>
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
                <img src="https://www.iriseupacademy.com/static/myapp/images/resource/author-6.png" alt="iRiseUp Academy Logo">
                <h1>Welcome to iRiseUp Academy, {user_email}!</h1>
            </div>

            <!-- Email Content -->
            <div class="content">
                <p>Hello {user_email},</p>
                <p>Your account has been successfully created. Below is your temporary password:</p>
                <p><strong>Temporary Password:</strong> {random_password}</p>
                <p>Please log in and update your password for security.</p>
                <a href="https://www.iriseupacademy.com/sign_in" class="button">Log In Now</a>
                <p>Best regards,<br><strong>The iRiseUp Academy Team</strong></p>
            </div>

            <!-- Email Footer -->
            <div class="footer">
                <p>iRiseUp Academy, Columbus, Ohio, USA | <a href="https://iriseupacademy.com/unsubscribe">Unsubscribe</a></p>
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

            # Ensure the amount is valid based on the selected plan
            amount = determine_amount_based_on_plan(selected_plan)
            if amount <= 0:
                return JsonResponse({"error": "Invalid plan selected."}, status=400)

            # Step 1: Create a new customer or retrieve the existing one
            customer_result = square_client.customers.create_customer(
                body={
                    "given_name": data.get('givenName'),
                    "family_name": data.get('familyName'),
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
            user, created = User.objects.get_or_create(
                username=user_email,
                defaults={'email': user_email}
            )

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


logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import SignInForm  # Import the form
import logging
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

def sign_in(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        logger.debug(f"User {request.user.username} tried to access the login page while already logged in.")
        return redirect('coursemenu')  # Redirect to the course menu or appropriate page
    
    if request.method == 'POST':
        form = SignInForm(request.POST)

        if form.is_valid():
            login_identifier = form.cleaned_data.get('login_identifier')
            password = form.cleaned_data.get('password')
            logger.debug(f"Attempting login for identifier: {login_identifier}")

            # Authenticate using username or email
            user = authenticate(request, username=login_identifier, password=password)

            if user is None:
                try:
                    user = User.objects.get(email=login_identifier)
                    user = authenticate(request, username=user.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                # Check if the user has logged in before
                if user.last_login is None:
                    logger.debug(f"First login detected for user: {user.username}")
                    login(request, user)
                    messages.info(request, 'Please change your password to continue.')
                    return redirect('password_change')
                else:
                    login(request, user)
                    logger.debug(f"Redirecting to course menu for user: {user.username}")
                    messages.success(request, f'Welcome back, {user.username}!')
                    return redirect('coursemenu')
            else:
                logger.error(f"Authentication failed for identifier: {login_identifier}")
                messages.error(request, 'Invalid username/email or password. Please try again.')
                return redirect('sign_in')

    else:
        form = SignInForm()

    return render(request, 'myapp/quiz/sign_in.html', {'form': form})


def sign_out(request):
    logout(request)  # This logs the user out
    return redirect('sign_in')  # Redirect to the sign-in page after logging out


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
    subject = 'Reset Your Password - iRiseUp Academy'
    from_email = 'hello@iriseupacademy.com'
    to_email = [user_email]

    # Plain text content for fallback
    text_content = (
        f"Dear {user_email},\n\n"
        "You're receiving this email because you requested a password reset.\n"
        "Please click the link below to reset your password:\n"
        f"https://www.iriseupacademy.com/reset/{uid}/{token}/\n\n"
        "If you didn’t request this, please ignore this email.\n"
        "Best regards,\n"
        "The iRiseUp Academy Team"
    )

    # HTML content for the email
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Reset Your Password - iRiseUp Academy</title>
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
                <img src="https://www.iriseupacademy.com/static/myapp/images/resource/author-6.png" alt="iRiseUp Academy Logo">
                <h1>Reset Your Password</h1>
            </div>

            <!-- Email Content -->
            <div class="content">
                <p>Hello {user_email},</p>
                <p>You requested a password reset for your account. Click the button below to reset it:</p>
                <a href="https://www.iriseupacademy.com/reset/{uid}/{token}/" class="button">Reset Password</a>
                <p>If you didn’t request this, please ignore this email.</p>
                <p>Best regards,<br><strong>The iRiseUp Academy Team</strong></p>
            </div>

            <!-- Email Footer -->
            <div class="footer">
                <p>iRiseUp Academy, Columbus, Ohio, USA | <a href="https://iriseupacademy.com/unsubscribe">Unsubscribe</a></p>
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

# views.py
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
