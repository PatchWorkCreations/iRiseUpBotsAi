from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.tasks import send_welcome_email  # Ensure this import is correct
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
