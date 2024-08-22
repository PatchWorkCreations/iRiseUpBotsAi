from django.shortcuts import render
import os


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


# myapp/views.py


from django.shortcuts import render, get_object_or_404
from .models import Course, SubCourse, Lesson

# views.py
from django.shortcuts import render

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
    return render(request, 'myapp/course_list/course_detail.html', {'course': course, 'sub_courses': sub_courses})

def sub_course_detail(request, sub_course_id):
    sub_course = get_object_or_404(SubCourse, id=sub_course_id)
    lessons = sub_course.lesson_set.all()
    return render(request, 'myapp/course_list/sub_course_detail.html', {'sub_course': sub_course, 'lessons': lessons})

def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'myapp/course_list/lesson_detail.html', {'lesson': lesson})
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Lesson
import json

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
    

from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from datetime import datetime, timedelta

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

from django.shortcuts import render, redirect

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
    if request.method == 'POST':
        return redirect('digital_business_knowledge')  # Replace with the next logical step in your flow
    return render(request, 'myapp/quiz/somewhat_interest.html')

def maybe_interest(request):
    if request.method == 'POST':
        return redirect('digital_business_knowledge')  # Replace with the next logical step in your flow
    return render(request, 'myapp/quiz/maybe_interest.html')

def not_necessarily_interest(request):
    if request.method == 'POST':
        return redirect('digital_business_knowledge')  # Replace with the next logical step in your flow
    return render(request, 'myapp/quiz/not_necessarily_interest.html')

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

from datetime import datetime, timedelta
from django.shortcuts import render, redirect

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

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailCollection
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages

def email_collection(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        receive_offers = request.POST.get('receive_offers') == 'on'  # Convert "on" to True, otherwise False

        try:
            # Attempt to create the email record
            EmailCollection.objects.create(email=email, receive_offers=receive_offers)
            
            # Prepare the email content
            subject = 'Welcome to iRiseUp.Ai!'
            html_message = render_to_string('welcome_email.html', {'email': email})
            plain_message = strip_tags(html_message)
            from_email = 'your-email@example.com'
            to = email

            # Send the welcome email
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)

            # Redirect to the readiness level page
            return redirect('readiness_level')

        except IntegrityError:
            # Handle the case where the email already exists
            messages.error(request, "This email is already registered. Please use a different email or log in.")
            return render(request, 'myapp/quiz/email_collection.html', {
                'email': email,
                'receive_offers': receive_offers,
            })

    return render(request, 'myapp/quiz/email_collection.html')

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_welcome_email(user_email):
    subject = 'Welcome to iRiseUp.Ai!'
    from_email = 'juliavictorio16@gmail.com'  # Replace with your actual email address
    to_email = [user_email]

    # Render HTML content from the template
    html_content = render_to_string('welcome_email.html', {'user_email': user_email})
    text_content = strip_tags(html_content)  # Strip the HTML tags for plain text alternative

    # Create the email object and attach the HTML content
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    
    # Send the email
    msg.send()


def readiness_level(request):
    if request.method == 'POST':
        # Process form submission or redirect
        return redirect('personalized_plan')  # Replace 'next_page' with the actual next page URL or name

    return render(request, 'myapp/quiz/readiness_level.html')  # Replace with the correct template path


from django.shortcuts import render

def personalized_plan(request):
    # Retrieve session data
    age = request.session.get('age_range', '')
    gender = request.session.get('gender', '')
    special_goal = request.session.get('special_goal', '')

    # Convert age to integer for comparison
    try:
        age = int(age.split('-')[0])  # Extracts the starting age from the range, e.g., "35-44" -> 35
    except (ValueError, IndexError):
        age = None  # Set age to None if there's an issue with age processing

    # Determine image path based on gender and age
    if gender == 'male':
        if age is not None and age < 30:
            current_image_path = 'myapp/images/male_before_young.png'
            goal_image_path = 'myapp/images/male_after_young.png'
        else:
            current_image_path = 'myapp/images/male_before_adult.png'
            goal_image_path = 'myapp/images/male_after_adult.png'
    else:
        if age is not None and age < 30:
            current_image_path = 'myapp/images/female_before_young.png'
            goal_image_path = 'myapp/images/female_after_young.png'
        else:
            current_image_path = 'myapp/images/female_before_adult.png'
            goal_image_path = 'myapp/images/female_after_adult.png'

    # Pass context data to the template
    context = {
        'current_image_path': current_image_path,
        'goal_image_path': goal_image_path,
        'special_goal': special_goal,
    }

    return render(request, 'myapp/quiz/personalized_plan.html', context)



from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid
import json
from .models import EmailCollection, Course, UserCourseAccess
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import logging
from django.utils import timezone
from datetime import timedelta
from .models import UserCourseAccess, Course
from square.client import Client
from django.conf import settings

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

from django.utils import timezone
from datetime import timedelta

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


import logging

# Get an instance of a logger
logger = logging.getLogger('myapp')

# Then your process_payment function should work as expected:
@csrf_exempt
def process_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            card_token = data.get('source_id')
            selected_plan = data.get('plan')

            amount = determine_amount_based_on_plan(selected_plan)

            if amount <= 0:
                return JsonResponse({"error": "Invalid plan selected."}, status=400)

            body = {
                "source_id": card_token,
                "idempotency_key": str(uuid.uuid4()),
                "amount_money": {
                    "amount": amount,
                    "currency": "USD"
                }
            }

            # Make the API request to Square
            result = client.payments.create_payment(body)

            # Log the raw response from Square API
            logger.info("Square API Response: %s", result)

            if result.is_success():
                user_email = EmailCollection.objects.filter(receive_offers=True).order_by('-id').first()
                if user_email:
                    random_password = get_random_string(8)

                    user, created = User.objects.get_or_create(
                        username=user_email.email,
                        email=user_email.email,
                    )
                    if created:
                        user.set_password(random_password)
                        user.save()

                        # Grant access to the course
                        grant_course_access(user, selected_plan)

                        subject = 'Your Account Has Been Created'
                        message = f'Your account has been created. Your temporary password is: {random_password}\nPlease log in and change your password.\nYou now have access to the course menu based on your selected plan.'
                        send_mail(subject, message, 'your-email@example.com', [user_email.email])

                return JsonResponse({"success": True})
            else:
                error_messages = [error['detail'] for error in result.errors]
                logger.error("Payment Error: %s", error_messages)
                return JsonResponse({"error": error_messages}, status=400)

        except Exception as e:
            logger.error("Unexpected error occurred: %s", str(e), exc_info=True)
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
import requests  # Ensure you have this imported
from myapp.services.paypal_client import PayPalClient
from myapp.models import EmailCollection, User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

# Initialize the logger
logger = logging.getLogger(__name__)

# Initialize PayPal client
paypal_client = PayPalClient(
    client_id=settings.PAYPAL_CLIENT_ID,
    client_secret=settings.PAYPAL_CLIENT_SECRET
)


@csrf_exempt
def create_paypal_order(request):
    if request.method == 'POST':
        try:
            selected_plan = request.POST.get('plan')

            if not selected_plan:
                return JsonResponse({"error": "Plan not provided"}, status=400)

            # Store the selected plan in the session
            request.session['selected_plan'] = selected_plan  # Ensure consistency here
            logger.info(f"Plan stored in session: {request.session.get('selected_plan')}")

            amount_cents = determine_amount_based_on_plan(selected_plan)
            if amount_cents <= 0:
                return JsonResponse({"error": "Invalid plan selected"}, status=400)

            amount_dollars = "{:.2f}".format(amount_cents / 100)

            order = {
                "intent": "CAPTURE",
                "purchase_units": [{
                    "amount": {
                        "currency_code": "USD",
                        "value": amount_dollars
                    }
                }],
                "application_context": {
                    "return_url": "https://iriseupai-production.up.railway.app/complete-paypal-payment/",
                    "cancel_url": "https://iriseupai-production.up.railway.app/payment/"
                }
            }

            # Make the request to PayPal API
            response = requests.post(
                f"https://api-m.sandbox.paypal.com/v2/checkout/orders",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {paypal_client.access_token}"
                },
                json=order
            )
            response.raise_for_status()

            order_response = response.json()

            # Safely extract the approval URL
            try:
                approval_url = next(link['href'] for link in order_response['links'] if link['rel'] == 'approve')
            except (KeyError, StopIteration):
                logger.error("Approval URL not found in PayPal response")
                return JsonResponse({"error": "Approval URL not found"}, status=500)

            return JsonResponse({"approval_url": approval_url})

        except Exception as e:
            logger.error("Failed to create PayPal order: %s", str(e))
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method."}, status=405)

import os
from django.conf import settings


@csrf_exempt
def complete_paypal_payment(request):
    if request.method == 'GET':
        try:
            order_id = request.GET.get('token')
            selected_plan = request.session.get('selected_plan')  # Ensure consistency here
            logger.info(f"Retrieved plan from session: {selected_plan}")

            if not order_id:
                logger.error("Missing order_id")
                return JsonResponse({'success': False, 'error': 'Missing order_id'}, status=400)

            if not selected_plan:
                logger.error("Selected plan not found in session.")
                return JsonResponse({'success': False, 'error': 'Selected plan not found in session.'}, status=400)

            # Check the order status before capturing
            order_details = paypal_client.get_order(order_id)
            order_status = order_details.get('status')
            logger.info(f"Order status: {order_status}")

            if order_status == 'COMPLETED' or order_status == 'APPROVED':
                # Capture the order if not already completed
                if order_status == 'APPROVED':
                    capture_response = paypal_client.capture_order(order_id)
                    logger.info(f"Capture response: {capture_response}")

                    if capture_response.get('status') != 'COMPLETED':
                        logger.error("Payment not completed: %s", capture_response)
                        return JsonResponse({'success': False, 'error': 'Payment not completed', 'response': capture_response})

                # Handle email notification and user account creation
                user_email = EmailCollection.objects.filter(receive_offers=True).order_by('-id').first()
                if user_email:
                    random_password = get_random_string(8)

                    # Create or retrieve the user
                    user, created = User.objects.get_or_create(
                        username=user_email.email,
                        email=user_email.email,
                    )
                    if created:
                        user.set_password(random_password)
                        user.save()

                        # Grant access to the course
                        grant_course_access(user, selected_plan)

                        # Send email notification
                        subject = 'Your Account Has Been Created'
                        message = f'Your account has been created. Your temporary password is: {random_password}\nPlease log in and change your password.\nYou now have access to the course menu based on your selected plan.'
                        send_mail(subject, message, 'your-email@example.com', [user_email.email])

                # Clear the selected plan from the session
                del request.session['selected_plan']  # Ensure you delete the correct key

                return JsonResponse({'success': True, 'message': 'Payment completed successfully.'})
            else:
                logger.error(f"Order not in a capturable state: {order_status}")
                return JsonResponse({'success': False, 'error': f'Order not in a capturable state: {order_status}'}, status=400)

        except Exception as e:
            logger.error("Error capturing PayPal order: %s", str(e))
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)



from django.shortcuts import render

def payment_page(request):
    return render(request, 'myapp/quiz/process_payment.html')

def success_page(request):
    return render(request, 'myapp/quiz/success.html')



def subscription_terms(request):
    return render(request, 'myapp/quiz/subscription_terms.html')

def terms_conditions(request):
    return render(request, 'myapp/quiz/terms_conditions.html')

def privacy_policy(request):
    return render(request, 'myapp/quiz/privacy_policy.html')  # Privacy Policy view

from django.shortcuts import render, get_object_or_404
from myapp.models import KnowledgeBaseCategory, KnowledgeBaseArticle

from django.shortcuts import render, get_object_or_404
from myapp.models import KnowledgeBaseCategory, KnowledgeBaseArticle, KnowledgeBaseSubCategory

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

from myapp.models import KnowledgeBaseCategory
from django.shortcuts import render

def knowledge_base(request):
    categories = KnowledgeBaseCategory.objects.prefetch_related('subcategories__articles').all()
    return render(request, 'myapp/quiz/support/knowledge_base.html', {'categories': categories})

from django.shortcuts import render, get_object_or_404
from myapp.models import KnowledgeBaseSubCategory

def subcategory_detail(request, id):
    subcategory = get_object_or_404(KnowledgeBaseSubCategory, id=id)
    articles = subcategory.articles.all()
    return render(request, 'myapp/quiz/support/subcategory_detail.html', {'subcategory': subcategory, 'articles': articles})


from django.shortcuts import render, get_object_or_404
from myapp.models import KnowledgeBaseArticle
import json

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


from django.shortcuts import render, get_object_or_404
from myapp.models import KnowledgeBaseCategory, KnowledgeBaseArticle

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



def coursemenu(request):
    all_courses = Course.objects.all()
    current_course_access = None
    current_course = None

    if request.user.is_authenticated:
        current_course_access = UserCourseAccess.objects.filter(user=request.user).first()

        if current_course_access and current_course_access.has_expired():
            # Access has expired, remove access
            current_course_access.delete()
            current_course_access = None
        else:
            current_course = current_course_access.course if current_course_access else None

    context = {
        'all_courses': all_courses,
        'current_course': current_course,
        'current_course_access': current_course_access,
    }
    return render(request, 'myapp/coursemenu.html', context)


def preview_email(request):
    user_email = 'test@example.com'  # Example email, you can customize this
    return render(request, 'welcome_email.html', {'user_email': user_email})



import logging
logger = logging.getLogger(__name__)

def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        logger.debug(f"Attempting login for email: {email}")

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            email_collection = EmailCollection.objects.filter(user=user).first()
            if email_collection and not email_collection.first_login_completed:
                logger.debug(f"First login detected for user: {user.username}")
                return redirect('change_password')
            else:
                logger.debug(f"Redirecting to course menu for user: {user.username}")
                return redirect('coursemenu')
        else:
            if EmailCollection.objects.filter(user__username=email).exists():
                logger.error(f"Incorrect password for email: {email}")
                messages.error(request, 'Incorrect password. Please try again.')
            else:
                logger.error(f"No account found for email: {email}")
                messages.error(request, 'No account found with this email. Please sign up.')
    
    return render(request, 'myapp/quiz/sign_in.html')


from django.contrib.auth import logout
from django.shortcuts import redirect

def sign_out(request):
    logout(request)  # This logs the user out
    return redirect('sign_in')  # Redirect to the sign-in page after logging out


from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from myapp.models import EmailCollection

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'myapp/change_password.html'
    success_url = reverse_lazy('coursemenu')  # Redirect to course menu after password change

    def form_valid(self, form):
        # Update password
        response = super().form_valid(form)
        
        # Mark first login as completed after password change
        email_collection = EmailCollection.objects.filter(user=self.request.user).first()
        if email_collection:
            email_collection.first_login_completed = True
            email_collection.save()

        return response


from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = 'myapp/forgot_password.html'
    email_template_name = 'myapp/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

from django.contrib.auth.views import PasswordResetDoneView

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'myapp/password_reset_done.html'


from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import render, redirect
from .forms import SubmitRequestForm

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import SubmitRequestForm

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
            to = email = 'juliavictorio16@gmail.com'

            # Send the email
            send_mail(
                email_subject,
                plain_message,
                from_email,
                [to],
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
