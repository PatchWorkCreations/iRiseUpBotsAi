from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta
import logging
import uuid
from square.client import Client
from django.conf import settings

logger = logging.getLogger(__name__)

# Initialize Square client
client = Client(
    access_token=settings.SQUARE_ACCESS_TOKEN,
    environment='sandbox',  # Change to 'production' when you're ready
)

@shared_task
def add(x, y):
    return x + y

import logging
from django.core.exceptions import ObjectDoesNotExist
from celery import shared_task
from myapp.models import Lesson, UserLessonProgress

# Set up a logger
logger = logging.getLogger(__name__)

from celery import shared_task
from myapp.models import Lesson, UserLessonProgress

@shared_task
def complete_lesson_task(user_id, lesson_id):
    try:
        # Fetch the lesson and user progress
        user_progress = UserLessonProgress.objects.select_related('lesson__parent_sub_course__parent_course').get(user_id=user_id, lesson_id=lesson_id)
        
        # If the lesson is not completed, mark it as completed
        if not user_progress.completed:
            user_progress.complete_lesson()

            # Unlock the next lesson
            lesson = Lesson.objects.get(id=lesson_id)
            UserLessonProgress.unlock_next_lesson(user_progress.user, lesson)
        
        return True
    except Exception as e:
        # Log any exceptions here
        print(f"Error in complete_lesson_task: {str(e)}")
        return False



@shared_task(name="send_welcome_email_task")
def send_welcome_email(email):
    subject = 'Welcome to iRiseUp.Ai!'
    html_message = render_to_string('welcome_email.html', {'email': email})
    plain_message = strip_tags(html_message)
    from_email = 'juliavictorio16@gmail.com'  # Replace with your actual sender email
    send_mail(subject, plain_message, from_email, [email], html_message=html_message)
    
    return f"'send_welcome_email_task' completed for {email}"


@shared_task(name="charge_card_for_renewal")
def charge_card_for_renewal(user_id=None):
    # Import models here to avoid the AppRegistryNotReady error
    from .models import SquareCustomer, UserCourseAccess
    from myapp.views import determine_amount_based_on_plan

    # Define the renewal period mapping
    renewal_periods = {
        '1-week': timedelta(weeks=1),
        '4-week': timedelta(weeks=4),
        '12-week': timedelta(weeks=12),
    }

    # Get the current time
    current_time = timezone.now()

    # If user_id is provided, get only that user's course access for testing
    if user_id:
        user_accesses = UserCourseAccess.objects.filter(user_id=user_id)
    else:
        # Otherwise, get all users whose expiration date is due for renewal
        renewal_window_start = current_time + timedelta(days=2)
        renewal_window_end = current_time + timedelta(days=1)
        user_accesses = UserCourseAccess.objects.filter(expiration_date__range=(renewal_window_start, renewal_window_end))

    if not user_accesses.exists():
        logger.info("No user courses due for renewal.")

    for user_access in user_accesses:
        try:
            square_customer = SquareCustomer.objects.get(user=user_access.user)

            # Determine the amount to charge based on the plan
            amount = determine_amount_based_on_plan(user_access.selected_plan)

            # Create a payment request using the stored card
            payment_result = client.payments.create_payment(
                body={
                    "source_id": square_customer.card_id,
                    "idempotency_key": str(uuid.uuid4()),
                    "amount_money": {
                        "amount": amount,
                        "currency": "USD"
                    },
                    "autocomplete": True,
                    "customer_id": square_customer.customer_id,
                }
            )

            if payment_result.is_error():
                error_messages = [error['detail'] for error in payment_result.errors]
                logger.error(f"Payment Error for user {user_access.user.email}: {error_messages}")
                continue  # Skip to the next user if payment fails

            # Assuming the charge is successful, extend the user's access
            renewal_period = renewal_periods.get(user_access.selected_plan, timedelta(weeks=4))  # Default to 4 weeks if plan is unrecognized
            user_access.expiration_date += renewal_period
            user_access.save()

            logger.info(f"Successfully charged and extended access for user {user_access.user.email}")

        except SquareCustomer.DoesNotExist:
            logger.error(f"SquareCustomer record not found for user {user_access.user.email}")
        except Exception as e:
            logger.error(f"Failed to charge card for user {user_access.user.email}: {str(e)}")




