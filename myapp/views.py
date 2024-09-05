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

def blogclassic(request):
    return render(request, 'myapp/blog-classic.html')

def blog(request):
    return render(request, 'myapp/blog.html')

def contact(request):
    return render(request, 'myapp/contact.html')

def faq(request):
    return render(request, 'myapp/faq.html')

def index2(request):
    return render(request, 'myapp/index-2.html')

def index3(request):
    return render(request, 'myapp/index-3.html')

def index(request):
    return render(request, 'myapp/index.html')


def newsdetail(request):
    return render(request, 'myapp/news-detail.html')

def notfound(request):
    return render(request, 'myapp/not-found.html')

def pricing(request):
    return render(request, 'myapp/pricing.html')

def register(request):
    return render(request, 'myapp/register.html')

def reset(request):
    return render(request, 'myapp/reset.html')

def servicedetail(request):
    return render(request, 'myapp/service-detail.html')

def services(request):
    return render(request, 'myapp/services.html')

def teamdetail(request):
    return render(request, 'myapp/team-detail.html')

def team(request):
    return render(request, 'myapp/team.html')

def testimonial(request):
    return render(request, 'myapp/testimonial.html')


def newsdetail1(request):
    return render(request, 'myapp/news-detail1.html')

def newsdetail2(request):
    return render(request, 'myapp/news-detail2.html')

def newsdetail3(request):
    return render(request, 'myapp/news-detail3.html')

def newsdetail4(request):
    return render(request, 'myapp/news-detail4.html')

def newsdetail5(request):
    return render(request, 'myapp/news-detail5.html')

def newsdetail6(request):
    return render(request, 'myapp/news-detail6.html')

def newsdetail7(request):
    return render(request, 'myapp/news-detail7.html')

def newsdetail8(request):
    return render(request, 'myapp/news-detail8.html')

def servicedetail1(request):
    return render(request, 'myapp/service-detail1.html')

def servicedetail2(request):
    return render(request, 'myapp/service-detail2.html')

def servicedetail3(request):
    return render(request, 'myapp/service-detail3.html')

def servicedetail4(request):
    return render(request, 'myapp/service-detail4.html')

def servicedetail5(request):
    return render(request, 'myapp/service-detail5.html')

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

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    sub_courses = course.sub_courses.all()  # Use the related name
    user_progress = {}

    if request.user.is_authenticated:
        for sub_course in sub_courses:
            lessons = sub_course.lessons.all()
            completed_lessons = lessons.filter(userlessonprogress__user=request.user, userlessonprogress__completed=True).count()
            user_progress[sub_course.id] = {
                'completed_lessons': completed_lessons,
                'total_lessons': lessons.count(),
                'sub_course_progress': UserSubCourseAccess.objects.filter(user=request.user, sub_course=sub_course).first()
            }

    context = {
        'course': course,
        'sub_courses': sub_courses,
        'user_progress': user_progress,
    }
    return render(request, 'myapp/course_list/course_detail.html', context)

def sub_course_detail(request, sub_course_id):
    sub_course = get_object_or_404(SubCourse, id=sub_course_id)
    lessons = sub_course.lesson_set.all()
    return render(request, 'myapp/course_list/sub_course_detail.html', {'sub_course': sub_course, 'lessons': lessons})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'myapp/course_list/lesson_detail.html', {'lesson': lesson})


def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course_detail_url = reverse('course_detail', args=[lesson.parent_sub_course.parent_course.id])
    
    # Debug: Print the lesson content
    print("Lesson Content:", lesson.content)
    
    try:
        content_blocks = json.loads(lesson.content)
    except json.JSONDecodeError as e:
        # Debug: Print the error
        print("JSON Decode Error:", e)
        content_blocks = []
    
    context = {
        'lesson': lesson,
        'course_detail_url': course_detail_url,
        'content_blocks': content_blocks,
    }
    return render(request, 'myapp/course_list/lesson_detail.html', context)


def next_lesson(request, lesson_id):
    current_lesson = get_object_or_404(Lesson, id=lesson_id)
    next_lesson = Lesson.objects.filter(parent_sub_course=current_lesson.parent_sub_course, id__gt=current_lesson.id).order_by('id').first()

    if next_lesson:
        return redirect('lesson_detail', lesson_id=next_lesson.id)
    else:
        return redirect('course_detail', course_id=current_lesson.parent_sub_course.parent_course.id)  # Redirect to course detail page
    
def coursemenu(request):
    all_courses = Course.objects.all()
    current_course_access = None
    current_course = None
    course_progress = {}

    if request.user.is_authenticated:
        current_course_access = UserCourseAccess.objects.filter(user=request.user, progress__gt=0).first()

        if current_course_access and current_course_access.has_expired():
            # Access has expired, remove access
            current_course_access.delete()
            current_course_access = None
        else:
            current_course = current_course_access.course if current_course_access else None

        for course in all_courses:
            sub_courses = course.sub_courses.all()
            sub_course_progress = {}
            for sub_course in sub_courses:
                lessons = sub_course.lessons.all()
                completed_lessons = lessons.filter(userlessonprogress__user=request.user, userlessonprogress__completed=True).count()
                sub_course_progress[sub_course.id] = {
                    'completed_lessons': completed_lessons,
                    'total_lessons': lessons.count(),
                    'progress': completed_lessons / lessons.count() * 100 if lessons.count() > 0 else 0
                }
            course_progress[course.id] = sub_course_progress

    context = {
        'all_courses': all_courses,
        'current_course': current_course,
        'current_course_access': current_course_access,
        'course_progress': course_progress,
    }
    return render(request, 'myapp/coursemenu.html', context)


def combined_quiz(request):
    current_step = request.session.get('current_step', 'start')
    
    if request.method == 'POST':
        if current_step == 'start':
            # Handle gender selection
            request.session['gender'] = request.POST.get('gender')
            request.session['current_step'] = 'age_selection'
        
        elif current_step == 'age_selection':
            # Handle age selection
            request.session['age_range'] = request.POST.get('age_range')
            request.session['current_step'] = 'after_age_page'
        
        elif current_step == 'after_age_page':
            # Move to main goal after age selection
            request.session['current_step'] = 'main_goal'
        
        elif current_step == 'main_goal':
            # Handle main goal selection
            request.session['main_goal'] = request.POST.get('main_goal')
            request.session['current_step'] = 'income_source'
        
        elif current_step == 'income_source':
            # Handle income source selection
            request.session['income_source'] = request.POST.get('income_source')
            request.session['current_step'] = 'work_schedule'
        
        elif current_step == 'work_schedule':
            # Handle work schedule selection
            request.session['work_schedule'] = request.POST.get('work_schedule')
            request.session['current_step'] = 'job_challenges'
        
        elif current_step == 'job_challenges':
            # Handle job challenges selection
            job_challenges = request.POST.getlist('job_challenges')
            request.session['job_challenges'] = job_challenges
            request.session['current_step'] = 'after_job_challenges_page'
        
        elif current_step == 'after_job_challenges_page':
            # Move to financial situation after job challenges
            request.session['current_step'] = 'financial_situation'
        
        elif current_step == 'financial_situation':
            # Handle financial situation selection
            financial_situation = request.POST.get('financial_situation')
            request.session['financial_situation'] = financial_situation

            if financial_situation == "I'm comfortable":
                request.session['current_step'] = 'comfortable_financial'
            elif financial_situation == "I would like to have more stability":
                request.session['current_step'] = 'stability_financial'
            elif financial_situation == "I'm struggling to meet my financial goals":
                request.session['current_step'] = 'struggling_financial'
        
        elif current_step in ['comfortable_financial', 'stability_financial', 'struggling_financial']:
            # After financial situation, move to annual income goal
            request.session['current_step'] = 'annual_income_goal'
        
        elif current_step == 'annual_income_goal':
            # Handle annual income goal selection
            request.session['annual_income_goal'] = request.POST.get('annual_income_goal')
            request.session['current_step'] = 'control_work_hours'
        
        elif current_step == 'control_work_hours':
            # Handle control of work hours selection
            request.session['control_work_hours'] = request.POST.get('control_work_hours')
            request.session['current_step'] = 'routine_work'
        
        elif current_step == 'routine_work':
            # Handle routine work selection
            request.session['routine_work'] = request.POST.get('routine_work')
            request.session['current_step'] = 'time_saved_use'
        
        elif current_step == 'time_saved_use':
            # Handle time saved use selection
            request.session['time_saved_use'] = request.POST.get('time_saved_use')
            request.session['current_step'] = 'job_interest_match'
        
        elif current_step == 'job_interest_match':
            # Handle job interest match selection
            job_interest_question = request.POST.get('job_interest_question')
            request.session['job_interest_question'] = job_interest_question

            if job_interest_question == 'Absolutely':
                request.session['current_step'] = 'absolutely_interest'
            elif job_interest_question == 'Somewhat':
                request.session['current_step'] = 'somewhat_interest'
            elif job_interest_question == 'Maybe':
                request.session['current_step'] = 'maybe_interest'
            elif job_interest_question == 'Not necessarily':
                request.session['current_step'] = 'not_necessarily_interest'
        
        elif current_step in ['absolutely_interest', 'somewhat_interest', 'maybe_interest', 'not_necessarily_interest']:
            # After job interest match, move to digital business knowledge
            request.session['current_step'] = 'digital_business_knowledge'
        
        elif current_step == 'digital_business_knowledge':
            # Handle digital business knowledge selection
            request.session['digital_business_knowledge'] = request.POST.get('digital_business_knowledge')
            request.session['current_step'] = 'side_hustle_experience'
        
        elif current_step == 'side_hustle_experience':
            # Handle side hustle experience selection
            request.session['side_hustle_experience'] = request.POST.get('side_hustle_experience')
            request.session['current_step'] = 'learning_new_skills'
        
        elif current_step == 'learning_new_skills':
            # Handle learning new skills selection
            request.session['learning_new_skills'] = request.POST.get('learning_new_skills')
            request.session['current_step'] = 'ai_tools_familiarity'
        
        elif current_step == 'ai_tools_familiarity':
            # Handle AI tools familiarity selection
            ai_tools_familiarity = request.POST.getlist('ai_tools_familiarity')
            request.session['ai_tools_familiarity'] = ai_tools_familiarity
            request.session['current_step'] = 'content_writing_knowledge'
        
        elif current_step == 'content_writing_knowledge':
            # Handle content writing knowledge selection
            request.session['content_writing_knowledge'] = request.POST.get('content_writing_knowledge')
            request.session['current_step'] = 'digital_marketing_knowledge'
        
        elif current_step == 'digital_marketing_knowledge':
            # Handle digital marketing knowledge selection
            request.session['digital_marketing_knowledge'] = request.POST.get('digital_marketing_knowledge')
            request.session['current_step'] = 'ai_income_boost_awareness'
        
        elif current_step == 'ai_income_boost_awareness':
            # Handle AI income boost awareness selection
            request.session['ai_income_boost_awareness'] = request.POST.get('ai_income_boost_awareness')
            request.session['current_step'] = 'fields_interest'
        
        elif current_step == 'fields_interest':
            # Handle fields of interest selection
            fields_interest = request.POST.getlist('fields_interest')
            request.session['fields_interest'] = fields_interest
            request.session['current_step'] = 'ai_mastery_readiness'
        
        elif current_step == 'ai_mastery_readiness':
            # Handle AI mastery readiness selection
            ai_mastery_readiness = request.POST.get('ai_mastery_readiness')
            request.session['ai_mastery_readiness'] = ai_mastery_readiness

            if ai_mastery_readiness == 'All set - I am fully prepared':
                request.session['current_step'] = 'all_set'
            elif ai_mastery_readiness == 'Ready - I feel confident':
                request.session['current_step'] = 'ready'
            elif ai_mastery_readiness == 'Somewhat Ready - I have some knowledge':
                request.session['current_step'] = 'somewhat_ready'
            elif ai_mastery_readiness == 'Not Ready - I need more preparation':
                request.session['current_step'] = 'not_ready'
        
        elif current_step in ['all_set', 'ready', 'somewhat_ready', 'not_ready']:
            # After AI mastery readiness, move to focus ability
            request.session['current_step'] = 'focus_ability'
        
        elif current_step == 'focus_ability':
            # Handle focus ability selection
            request.session['focus_ability'] = request.POST.get('focus_ability')
            request.session['current_step'] = 'summary'
        
        elif current_step == 'summary':
            # Move to the special goal step
            request.session['current_step'] = 'special_goal'
        
        elif current_step == 'special_goal':
            # Handle special goal selection
            request.session['special_goal'] = request.POST.get('special_goal')
            request.session['current_step'] = 'time_to_achieve_goal'
        
        elif current_step == 'time_to_achieve_goal':
            # Handle time to achieve goal selection
            request.session['time_to_achieve_goal'] = request.POST.get('time_to_achieve_goal')
            return redirect('results')  # Final step, redirect to results page

    # Prepare context for rendering the current step
    context = {
        'current_step': current_step,
        'gender': request.session.get('gender'),
        'age_range': request.session.get('age_range'),
        'main_goal': request.session.get('main_goal'),
        'income_source': request.session.get('income_source'),
        'work_schedule': request.session.get('work_schedule'),
        'job_challenges': request.session.get('job_challenges'),
        'financial_situation': request.session.get('financial_situation'),
        'annual_income_goal': request.session.get('annual_income_goal'),
        'control_work_hours': request.session.get('control_work_hours'),
        'routine_work': request.session.get('routine_work'),
        'time_saved_use': request.session.get('time_saved_use'),
        'job_interest_question': request.session.get('job_interest_question'),
        'digital_business_knowledge': request.session.get('digital_business_knowledge'),
        'side_hustle_experience': request.session.get('side_hustle_experience'),
        'learning_new_skills': request.session.get('learning_new_skills'),
        'ai_tools_familiarity': request.session.get('ai_tools_familiarity'),
        'content_writing_knowledge': request.session.get('content_writing_knowledge'),
        'digital_marketing_knowledge': request.session.get('digital_marketing_knowledge'),
        'ai_income_boost_awareness': request.session.get('ai_income_boost_awareness'),
        'fields_interest': request.session.get('fields_interest'),
        'ai_mastery_readiness': request.session.get('ai_mastery_readiness'),
        'focus_ability': request.session.get('focus_ability'),
    }
    
    return render(request, 'myapp/quiz/combined_quiz.html', context)


def start_quiz(request):
    if request.method == 'POST':
        gender = request.POST.get('gender')
        request.session['gender'] = gender
        return redirect('age_selection')
    return render(request, 'myapp/quiz/start.html')

def age_selection(request):
    if request.method == 'POST':
        age_range = request.POST.get('age_range')
        request.session['age_range'] = age_range
        return redirect('after_age_page')
    gender = request.session.get('gender')
    context = {'gender': gender}
    return render(request, 'myapp/quiz/age_selection.html', context)


def after_age_page(request):
    if request.method == 'POST':
        return redirect('main_goal')
    return render(request, 'myapp/quiz/after_age_page.html')


def main_goal(request):
    # Ensure that gender is stored in the session
    gender = request.session.get('gender')
    
    if request.method == 'POST':
        # Save the main goal to the session
        request.session['main_goal'] = request.POST.get('main_goal')
        return redirect('income_source')
    
    # Pass the gender to the template
    return render(request, 'myapp/quiz/main_goal.html', {'gender': gender})


def income_source(request):
    if request.method == 'POST':
        request.session['income_source'] = request.POST.get('income_source')
        return redirect('work_schedule')
    return render(request, 'myapp/quiz/income_source.html')

def work_schedule(request):
    if request.method == 'POST':
        request.session['work_schedule'] = request.POST.get('work_schedule')
        return redirect('job_challenges')
    return render(request, 'myapp/quiz/work_schedule.html')

def job_challenges(request):
    if request.method == 'POST':
        job_challenges = request.POST.getlist('job_challenges')
        request.session['job_challenges'] = job_challenges
        return redirect('after_job_challenges_page')
    return render(request, 'myapp/quiz/job_challenges.html')


def after_job_challenges_page(request):
    if request.method == 'POST':
        return redirect('financial_situation')
    return render(request, 'myapp/quiz/after_job_challenges_page.html')


def financial_situation(request):
    if request.method == 'POST':
        financial_situation = request.POST.get('financial_situation')
        request.session['financial_situation'] = financial_situation

        if financial_situation == "I'm comfortable":
            return redirect('comfortable_financial')
        elif financial_situation == "I would like to have more stability":
            return redirect('stability_financial')
        elif financial_situation == "I'm struggling to meet my financial goals":
            return redirect('struggling_financial')
    return render(request, 'myapp/quiz/financial_situation.html')


def comfortable_financial(request):
    gender = request.session.get('gender')  # Retrieve gender from session
    if request.method == 'POST':
        return redirect('annual_income_goal')
    return render(request, 'myapp/quiz/comfortable_financial.html', {'gender': gender})

def stability_financial(request):
    gender = request.session.get('gender')  # Retrieve gender from session
    if request.method == 'POST':
        return redirect('annual_income_goal')
    return render(request, 'myapp/quiz/stability_financial.html', {'gender': gender})

def struggling_financial(request):
    gender = request.session.get('gender')  # Retrieve gender from session
    if request.method == 'POST':
        return redirect('annual_income_goal')
    return render(request, 'myapp/quiz/struggling_financial.html', {'gender': gender})


def annual_income_goal(request):
    # Retrieve gender from the session, assuming it was set earlier in the quiz flow
    gender = request.session.get('gender')

    if request.method == 'POST':
        # Save the user's selected annual income goal to the session
        request.session['annual_income_goal'] = request.POST.get('annual_income_goal')

        # Redirect to the next step in the quiz flow
        return redirect('control_work_hours')

    # Render the template with the gender context to conditionally show the correct image
    return render(request, 'myapp/quiz/annual_income_goal.html', {'gender': gender})

def control_work_hours(request):
    if request.method == 'POST':
        request.session['control_work_hours'] = request.POST.get('control_work_hours')
        return redirect('routine_work')
    return render(request, 'myapp/quiz/control_work_hours.html')


def routine_work(request):
    gender = request.session.get('gender')
    if request.method == 'POST':
        # Capture the user's response and store it in the session
        request.session['routine_work'] = request.POST.get('routine_work')
        
        # Redirect to the next step in the quiz, which is 'time_saved_use'
        return redirect('time_saved_use')
    
    # If it's a GET request, render the routine work quiz page
    return render(request, 'myapp/quiz/routine_work.html', {'gender': gender})

def time_saved_use(request):
    if request.method == 'POST':
        request.session['time_saved_use'] = request.POST.get('time_saved_use')
        return redirect('job_interest_match')
    return render(request, 'myapp/quiz/time_saved_use.html')


def job_interest_match(request):
    if request.method == 'POST':
        # Get the value from the POST request
        job_interest_question = request.POST.get('job_interest_question')
        
        # Store the selected value in the session if you need it for later use
        request.session['job_interest_question'] = job_interest_question
        
        # Redirect based on the value of job_interest_question
        if job_interest_question == 'Absolutely':
            return redirect('absolutely_interest')
        elif job_interest_question == 'Somewhat':
            return redirect('somewhat_interest')
        elif job_interest_question == 'Maybe':
            return redirect('maybe_interest')
        elif job_interest_question == 'Not necessarily':
            return redirect('not_necessarily_interest')
    
    # Render the initial form if the request method is GET
    return render(request, 'myapp/quiz/job_interest_match.html')

def absolutely_interest(request):
    # Assuming 'gender' is stored in the session from a previous step
    gender = request.session.get('gender', 'Male')  # Default to 'Male' if not set

    if request.method == 'POST':
        return redirect('digital_business_knowledge')  # Replace with the next logical step in your flow

    # Pass the gender to the template
    return render(request, 'myapp/quiz/absolutely_interest.html', {'gender': gender})


def somewhat_interest(request):
    gender = request.session.get('gender', 'Male')  # Default to 'Male' if not set

    if request.method == 'POST':
        return redirect('digital_business_knowledge')  # Replace with the next logical step in your flow

    return render(request, 'myapp/quiz/somewhat_interest.html', {'gender': gender})


def maybe_interest(request):
    gender = request.session.get('gender', 'Male')  # Default to 'Male' if not set

    if request.method == 'POST':
        return redirect('digital_business_knowledge')  # Replace with the next logical step in your flow

    return render(request, 'myapp/quiz/maybe_interest.html', {'gender': gender})


def not_necessarily_interest(request):
    gender = request.session.get('gender', 'Male')  # Default to 'Male' if not set

    if request.method == 'POST':
        return redirect('digital_business_knowledge')  # Replace with the next logical step in your flow

    return render(request, 'myapp/quiz/not_necessarily_interest.html', {'gender': gender})

def digital_business_knowledge(request):
    if request.method == 'POST':
        request.session['digital_business_knowledge'] = request.POST.get('digital_business_knowledge')
        return redirect('side_hustle_experience')
    return render(request, 'myapp/quiz/digital_business_knowledge.html')

def side_hustle_experience(request):
    if request.method == 'POST':
        request.session['side_hustle_experience'] = request.POST.get('side_hustle_experience')
        return redirect('learning_new_skills')
    return render(request, 'myapp/quiz/side_hustle_experience.html')

def learning_new_skills(request):
    if request.method == 'POST':
        request.session['learning_new_skills'] = request.POST.get('learning_new_skills')
        return redirect('ai_tools_familiarity')
    return render(request, 'myapp/quiz/learning_new_skills.html')

def ai_tools_familiarity(request):
    if request.method == 'POST':
        ai_tools_familiarity = request.POST.getlist('ai_tools_familiarity')
        request.session['ai_tools_familiarity'] = ai_tools_familiarity
        return redirect('content_writing_knowledge')
    return render(request, 'myapp/quiz/ai_tools_familiarity.html')

def content_writing_knowledge(request):
    if request.method == 'POST':
        request.session['content_writing_knowledge'] = request.POST.get('content_writing_knowledge')
        return redirect('digital_marketing_knowledge')
    return render(request, 'myapp/quiz/content_writing_knowledge.html')

def digital_marketing_knowledge(request):
    if request.method == 'POST':
        request.session['digital_marketing_knowledge'] = request.POST.get('digital_marketing_knowledge')
        return redirect('ai_income_boost_awareness')
    return render(request, 'myapp/quiz/digital_marketing_knowledge.html')

def ai_income_boost_awareness(request):
    if request.method == 'POST':
        request.session['ai_income_boost_awareness'] = request.POST.get('ai_income_boost_awareness')
        return redirect('fields_interest')
    return render(request, 'myapp/quiz/ai_income_boost_awareness.html')

def fields_interest(request):
    if request.method == 'POST':
        fields_interest = request.POST.getlist('fields_interest')
        request.session['fields_interest'] = fields_interest
        return redirect('ai_mastery_readiness')
    return render(request, 'myapp/quiz/fields_interest.html')


def ai_mastery_readiness(request):
    if request.method == 'POST':
        ai_mastery_readiness = request.POST.get('ai_mastery_readiness')
        print(f"Selected option: {ai_mastery_readiness}")  # Debugging print
        request.session['ai_mastery_readiness'] = ai_mastery_readiness

        if ai_mastery_readiness == 'All set - I am fully prepared':
            return redirect('all_set')
        elif ai_mastery_readiness == 'Ready - I feel confident':
            return redirect('ready')
        elif ai_mastery_readiness == 'Somewhat Ready - I have some knowledge':
            return redirect('somewhat_ready')
        elif ai_mastery_readiness == 'Not Ready - I need more preparation':
            return redirect('not_ready')

    return render(request, 'myapp/quiz/ai_mastery_readiness.html')


def all_set(request):
    if request.method == 'POST':
        return redirect('focus_ability')
    return render(request, 'myapp/quiz/all_set.html', {'gender': request.session.get('gender')})

def ready(request):
    if request.method == 'POST':
        return redirect('focus_ability')
    return render(request, 'myapp/quiz/ready.html', {'gender': request.session.get('gender')})

def somewhat_ready(request):
    if request.method == 'POST':
        return redirect('focus_ability')
    return render(request, 'myapp/quiz/somewhat_ready.html', {'gender': request.session.get('gender')})

def not_ready(request):
    if request.method == 'POST':
        return redirect('focus_ability')
    return render(request, 'myapp/quiz/not_ready.html', {'gender': request.session.get('gender')})


def focus_ability(request):
    if request.method == 'POST':
        request.session['focus_ability'] = request.POST.get('focus_ability')
        return redirect('summary')
    return render(request, 'myapp/quiz/focus_ability.html')

def summary(request):
    gender = request.session.get('gender', 'male').lower()
    
    # Determine the appropriate image path based on gender
    if gender == 'male':
        image_path = "myapp/images/quiz/male_be_my_own_boss.webp"
    else:  # Assuming the only other option is female
        image_path = "myapp/images/quiz/female_be_my_own_boss.webp"

    context = {
        'gender': gender,
        'age_range': request.session.get('age_range', '35-44'),
        'main_goal': request.session.get('main_goal', ''),
        'income_source': request.session.get('income_source', ''),
        'work_schedule': request.session.get('work_schedule', ''),
        'job_challenges': request.session.get('job_challenges', []),
        'financial_situation': request.session.get('financial_situation', ''),
        'annual_income_goal': request.session.get('annual_income_goal', ''),
        'control_work_hours': request.session.get('control_work_hours', ''),
        'routine_work': request.session.get('routine_work', ''),
        'time_saved_use': request.session.get('time_saved_use', ''),
        'job_interest_match': request.session.get('job_interest_match', ''),
        'digital_business_knowledge': request.session.get('digital_business_knowledge', ''),
        'side_hustle_experience': request.session.get('side_hustle_experience', ''),
        'learning_new_skills': request.session.get('learning_new_skills', ''),
        'ai_tools_familiarity': request.session.get('ai_tools_familiarity', []),
        'content_writing_knowledge': request.session.get('content_writing_knowledge', ''),
        'digital_marketing_knowledge': request.session.get('digital_marketing_knowledge', ''),
        'ai_income_boost_awareness': request.session.get('ai_income_boost_awareness', ''),
        'fields_interest': request.session.get('fields_interest', []),
        'ai_mastery_readiness': request.session.get('ai_mastery_readiness', ''),
        'focus_ability': request.session.get('focus_ability', ''),
        'special_goal': request.session.get('special_goal', ''),
        'time_to_achieve_goal': request.session.get('time_to_achieve_goal', ''),
        'profile_image': image_path,

        # Assuming these are derived or stored session values
        'motivation': request.session.get('motivation', 'High'),
        'potential': request.session.get('potential', 'High'),
        'focus': request.session.get('focus', 'Limited'),
        'ai_knowledge': request.session.get('ai_knowledge', 'Low'),
    }
    
    if request.method == 'POST':
        return redirect('special_goal')
    
    return render(request, 'myapp/quiz/summary.html', context)

def special_goal(request):
    if request.method == 'POST':
        request.session['special_goal'] = request.POST.get('special_goal')
        return redirect('time_to_achieve_goal')
    return render(request, 'myapp/quiz/special_goal.html')

def time_to_achieve_goal(request):
    if request.method == 'POST':
        request.session['time_to_achieve_goal'] = request.POST.get('time_to_achieve_goal')
        return redirect('results')  
    return render(request, 'myapp/quiz/time_to_achieve_goal.html')

from .models import QuizResponse

def save_quiz_response(request, user):
    # Retrieve all the session data
    gender = request.session.get('gender', '')
    age_range = request.session.get('age_range', '')
    main_goal = request.session.get('main_goal', '')
    income_source = request.session.get('income_source', '')
    work_schedule = request.session.get('work_schedule', '')
    job_challenges = request.session.get('job_challenges', [])
    financial_situation = request.session.get('financial_situation', '')
    annual_income_goal = request.session.get('annual_income_goal', '')
    control_work_hours = request.session.get('control_work_hours', '')
    routine_work = request.session.get('routine_work', '')
    time_saved_use = request.session.get('time_saved_use', '')
    job_interest_match = request.session.get('job_interest_question', '')
    digital_business_knowledge = request.session.get('digital_business_knowledge', '')
    side_hustle_experience = request.session.get('side_hustle_experience', '')
    learning_new_skills = request.session.get('learning_new_skills', '')
    ai_tools_familiarity = request.session.get('ai_tools_familiarity', [])
    content_writing_knowledge = request.session.get('content_writing_knowledge', '')
    digital_marketing_knowledge = request.session.get('digital_marketing_knowledge', '')
    ai_income_boost_awareness = request.session.get('ai_income_boost_awareness', '')
    fields_interest = request.session.get('fields_interest', [])
    ai_mastery_readiness = request.session.get('ai_mastery_readiness', '')
    focus_ability = request.session.get('focus_ability', '')
    special_goal = request.session.get('special_goal', '')
    time_to_achieve_goal = request.session.get('time_to_achieve_goal', '')

    # Create the QuizResponse instance associated with the authenticated user
    quiz_response = QuizResponse(
        user=user,  # Use the user object passed to the function
        gender=gender,
        age_range=age_range,
        main_goal=main_goal,
        income_source=income_source,
        work_schedule=work_schedule,
        job_challenges=job_challenges,
        financial_situation=financial_situation,
        annual_income_goal=annual_income_goal,
        control_work_hours=control_work_hours,
        enjoy_routine_job=routine_work,
        time_saved_use=time_saved_use,
        job_interest_match=job_interest_match,
        digital_business_knowledge=digital_business_knowledge,
        side_hustle_experience=side_hustle_experience,
        learning_new_skills=learning_new_skills,
        ai_tools_familiarity=ai_tools_familiarity,
        content_writing_knowledge=content_writing_knowledge,
        digital_marketing_knowledge=digital_marketing_knowledge,
        ai_income_boost_awareness=ai_income_boost_awareness,
        fields_interest=fields_interest,
        ai_mastery_readiness=ai_mastery_readiness,
        focus_ability=focus_ability,
        special_goal=special_goal,
        time_to_achieve_goal=time_to_achieve_goal,
        email=request.session.get('email', ''),  # Email from session
        receive_offers=request.session.get('receive_offers', False)
    )

    # Save the instance to the database
    quiz_response.save()


def results(request):

    # Get the current date
    current_date = datetime.now()

    # Get the current month
    current_month = current_date.month

    # Calculate the target month, which is two months from now
    target_date = current_date + timedelta(days=60)
    target_month = target_date.strftime('%b, %Y')  # Format as "Month, Year"

    # Store the context in the session for use after the loading page
    request.session['results_context'] = {
        'current_month': current_month,
        'target_month': target_month,
        'special_goal': request.session.get('special_goal', 'Your Goal'),
    }

    # Redirect to the loading page
    return redirect('loading_page')

def loading_page(request):
    return render(request, 'myapp/quiz/loading_page.html')

from django.db import IntegrityError, transaction
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import EmailCollection
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

logger = logging.getLogger(__name__)

# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.tasks import send_welcome_email  # Ensure this import is correct
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

        # Send the welcome email asynchronously
        send_welcome_email.delay(email)

        # Store the email in the session for later use during payment
        request.session['email'] = email

        return redirect('readiness_level')

    return render(request, 'myapp/quiz/email_collection.html')



def readiness_level(request):
    if request.method == 'POST':
        # Process form submission or redirect
        return redirect('personalized_plan')  # Replace 'next_page' with the actual next page URL or name

    return render(request, 'myapp/quiz/readiness_level.html')  # Replace with the correct template path



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

    return render(request, 'myapp/quiz/personalized_plan.html', context)


# Initialize the Square Client
client = Client(
    access_token=settings.SQUARE_ACCESS_TOKEN,  # Securely retrieved from environment variables
    environment='sandbox'  # Use 'production' for live transactions
)

def determine_amount_based_on_plan(plan):
    if plan == '1-week':
        return 1386  # $13.86 in cents
    elif plan == '4-week':
        return 3999  # $39.99 in cents
    elif plan == '12-week':
        return 7999  # $79.99 in cents
    else:
        return 0


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
    environment='sandbox',  # Change to 'production' when you're ready
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
            user_email = request.session.get('email')
            if not user_email:
                logger.error("Email is missing from session. Cannot proceed with payment.")
                return JsonResponse({"error": "Email is missing from session."}, status=400)

            # Ensure the amount is valid based on the selected plan
            amount = determine_amount_based_on_plan(selected_plan)
            if amount <= 0:
                return JsonResponse({"error": "Invalid plan selected."}, status=400)

            # Step 1: Create a new customer or retrieve the existing one
            customer_result = client.customers.create_customer(
                body={
                    "given_name": data.get('givenName'),
                    "family_name": data.get('familyName'),
                    "email_address": user_email,
                }
            )
            if customer_result.is_error():
                logger.error("Customer creation failed: %s", customer_result.errors)
                return JsonResponse({"error": "Failed to create customer profile."}, status=400)

            customer_id = customer_result.body['customer']['id']

            # Step 2: Make the payment request with the verification token and store the card on file
            payment_result = client.payments.create_payment(
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

            if payment_result.is_error():
                error_messages = [error['detail'] for error in payment_result.errors]
                logger.error("Payment Error: %s", error_messages)
                return JsonResponse({"error": error_messages}, status=400)

            payment_id = payment_result.body['payment']['id']

            # Step 3: Store the card on file for the customer
            card_result = client.cards.create_card(
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
                return JsonResponse({"error": "Failed to store card on file."}, status=400)

            card_id = card_result.body['card']['id']

            # Step 4: Create or retrieve the user in the Django application
            user, created = User.objects.get_or_create(
                username=user_email,
                defaults={'email': user_email}
            )

            if created:
                # If the user was created, set a random password and send an email
                random_password = get_random_string(8)
                user.set_password(random_password)
                user.save()

                # Send a welcome email with the temporary password
                subject = 'Your Account Has Been Created'
                message = (
                    f'Your account has been created. Your temporary password is: {random_password}\n'
                    'Please log in and change your password.\n'
                    'You now have access to the course menu based on your selected plan.'
                )
                send_mail(subject, message, 'juliavictorio16@Gmail.com', [user_email])

            logger.info(f"User {user_email} processed for payment.")

            # Step 5: Save the quiz response to the database linked with the user
            save_quiz_response(request, user)

            # Step 6: Store the customer_id and card_id in the database
            SquareCustomer.objects.update_or_create(
                user=user,
                defaults={'customer_id': customer_id, 'card_id': card_id}
            )

            # Step 7: Schedule the renewal if needed
            if selected_plan in ['1-week', '4-week', '12-week']:
                renewal_date = timezone.now() + timedelta(weeks=int(selected_plan.split('-')[0]))
                user_course_access = UserCourseAccess.objects.create(
                    user=user,
                    expiration_date=renewal_date
                )

            return JsonResponse({"success": True})

        except Exception as e:
            # Handle unexpected errors and log them
            logger.error("Unexpected error occurred: %s", str(e), exc_info=True)
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


# Initialize the logger
logger = logging.getLogger(__name__)

# Initialize PayPal client
paypal_client = PayPalClient(
    client_id=settings.PAYPAL_CLIENT_ID,
    client_secret=settings.PAYPAL_CLIENT_SECRET
)


from django.http import JsonResponse
from .paypal_utils import create_paypal_product, create_paypal_subscription_plan

def create_paypal_product_view(request):
    if request.method == "POST":
        product_id = create_paypal_product()
        if product_id:
            return JsonResponse({"success": True, "product_id": product_id})
        else:
            return JsonResponse({"success": False, "error": "Failed to create PayPal product."})
    return JsonResponse({"error": "Invalid request method."}, status=405)

from django.http import JsonResponse
from django.urls import reverse
from .paypal_utils import create_paypal_subscription_plan

def create_paypal_subscription_plan_view(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        plan_name = request.POST.get('plan_name')
        interval_unit = request.POST.get('interval_unit')
        interval_count = int(request.POST.get('interval_count'))
        amount = int(request.POST.get('amount'))  # amount in cents

        if not all([product_id, plan_name, interval_unit, interval_count, amount]):
            return JsonResponse({"error": "Missing required fields."}, status=400)

        # Dynamically generate the return_url and cancel_url using Django's reverse function
        return_url = request.build_absolute_uri(reverse('success_page'))  # Points to your success view
        cancel_url = request.build_absolute_uri(reverse('payment_page'))  # Points to your cancel page

        # Call your utility function with the return_url and cancel_url
        plan_id = create_paypal_subscription_plan(
            product_id, 
            plan_name, 
            interval_unit, 
            interval_count, 
            amount,
            return_url,  # Pass the generated return_url
            cancel_url   # Pass the generated cancel_url
        )

        if plan_id:
            return JsonResponse({"success": True, "plan_id": plan_id})
        else:
            return JsonResponse({"success": False, "error": "Failed to create PayPal subscription plan."})

    return JsonResponse({"error": "Invalid request method."}, status=405)

import json  # Make sure to import json for handling request data
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.utils import timezone
from django.http import JsonResponse
from .models import User, Subscription, UserCourseAccess
import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

def complete_paypal_subscription(request):
    if request.method == 'GET':
        try:
            # Log the PayPal response for debugging
            logger.info(f"PayPal return request: {request.GET}")

            # Get subscription ID from PayPal
            subscription_id = request.GET.get('subscription_id')
            user_email = request.session.get('email')  # Get user email from session

            if not subscription_id:
                return JsonResponse({'success': False, 'error': 'Missing subscription ID'}, status=400)

            if not user_email:
                return JsonResponse({'success': False, 'error': 'Email is missing from session.'}, status=400)

            # Create or retrieve the user
            user, created = User.objects.get_or_create(
                username=user_email,
                defaults={'email': user_email}
            )

            if created:
                # Generate random password for newly created users
                random_password = get_random_string(8)
                user.set_password(random_password)
                user.save()

                # Send email with account details
                subject = 'Your Account Has Been Created'
                message = f'Your temporary password is: {random_password}\nPlease log in and change your password.'
                send_mail(subject, message, 'your-email@example.com', [user_email])

            # Ensure the selected plan exists in the session
            selected_plan = request.session.get('selected_plan')
            if not selected_plan:
                return JsonResponse({'success': False, 'error': 'Selected plan is missing from session.'}, status=400)

            # Check if a subscription with the same subscription_id already exists
            if Subscription.objects.filter(subscription_id=subscription_id).exists():
                return JsonResponse({'success': False, 'error': 'This subscription ID already exists.'}, status=400)

            # Save subscription details
            Subscription.objects.create(
                user=user,
                subscription_id=subscription_id,
                plan=selected_plan
            )

            # Grant course access based on the selected plan
            if selected_plan == '1-week':
                expiration_date = timezone.now() + timedelta(weeks=1)
            elif selected_plan == '4-week':
                expiration_date = timezone.now() + timedelta(weeks=4)
            elif selected_plan == '12-week':
                expiration_date = timezone.now() + timedelta(weeks=12)
            else:
                return JsonResponse({'success': False, 'error': 'Invalid plan selected.'}, status=400)

            # Save course access with expiration
            UserCourseAccess.objects.create(user=user, expiration_date=expiration_date)

            # Clear session data
            request.session.pop('selected_plan', None)

            return JsonResponse({'success': True, 'message': 'Subscription completed successfully.'})

        except KeyError as e:
            logger.error(f"Missing key in session or request: {str(e)}", exc_info=True)
            return JsonResponse({'success': False, 'error': 'Invalid data received.'}, status=400)
        except Exception as e:
            logger.error(f"Error completing PayPal subscription: {str(e)}", exc_info=True)
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

def set_selected_plan(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_plan = data.get('plan')

            # Validate the selected plan
            valid_plans = ['1-week', '4-week', '12-week']
            if selected_plan in valid_plans:
                request.session['selected_plan'] = selected_plan
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid plan selected.'}, status=400)

        except Exception as e:
            logger.error(f"Error setting selected plan: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

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

logger = logging.getLogger(__name__)
def sign_in(request):
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
    template_name = 'myapp/password_change_done.html'


@receiver(post_save, sender=User)
def create_email_collection(sender, instance, created, **kwargs):
    if created:
        EmailCollection.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_email_collection(sender, instance, **kwargs):
    instance.email_collection.save()  # Use the related_name 'email_collection'


class CustomPasswordResetView(PasswordResetView):
    template_name = 'myapp/forgot_password.html'
    email_template_name = 'myapp/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'myapp/password_reset_done.html'


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
        return render(request, 'myapp/password_reset_confirm.html', {'form': form})
    else:
        # Invalid link
        return render(request, 'myapp/password_reset_invalid.html')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'myapp/password_reset_complete.html'


class CustomPasswordChangeDoneView(TemplateView):
    template_name = 'myapp/password_change_done.html'

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
            from_email = 'juliavictorio16@gmail.com'  # Replace with your email
            to = 'juliavictorio16@gmail.com'  # Send to yourself

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
    comments = post.forum_comments.filter(parent=None)
    form = ForumCommentForm()

    if request.method == 'POST':
        form = ForumCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return redirect('forum_post_detail', post_id=post.id)

    return render(request, 'myapp/forum/forum_post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


from django.shortcuts import render, redirect
from .models import ForumPost, ForumCategory
from .forms import ForumPostForm
from django.contrib import messages

def create_forum_post(request):
    if request.method == 'POST':
        # Copy POST data to mutable data
        post_data = request.POST.copy()
        new_category_name = post_data.get('new_category')

        if new_category_name:
            # Create the new category if it doesn't exist
            category, created = ForumCategory.objects.get_or_create(name=new_category_name)
            # Set the category ID in the form data to the newly created category
            post_data['category'] = category.id

        # Bind the form with the modified data
        form = ForumPostForm(post_data)

        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(request, "Your post has been created successfully.")
            return redirect('forum_post_detail', post_id=form.instance.id)
        else:
            messages.error(request, "There was an error with your submission. Please check the form.")
            print(form.errors)  # For debugging
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


@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'myapp/forum/edit_profile.html', {'form': form})

@login_required
def edit_avatar(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AvatarForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AvatarForm(instance=user_profile)
    return render(request, 'myapp/forum/edit_avatar.html', {'form': form, 'user_profile': user_profile})
