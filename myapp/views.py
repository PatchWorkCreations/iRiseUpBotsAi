from django.shortcuts import render

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

def login(request):
    return render(request, 'myapp/login.html')

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
from django.shortcuts import render
from .models import Course, UserCourseAccess

def coursemenu(request):
    all_courses = Course.objects.all()
    current_course_access = None
    current_course = None

    if request.user.is_authenticated:
        current_course_access = UserCourseAccess.objects.filter(user=request.user).first()
        current_course = current_course_access.course if current_course_access else None

    context = {
        'all_courses': all_courses,
        'current_course': current_course,
        'current_course_access': current_course_access,
    }
    return render(request, 'myapp/coursemenu.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Course, SubCourse, Lesson

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
        return redirect('main_goal')
    gender = request.session.get('gender')
    context = {'gender': gender}
    return render(request, 'myapp/quiz/age_selection.html', context)

def main_goal(request):
    if request.method == 'POST':
        request.session['main_goal'] = request.POST.get('main_goal')
        return redirect('income_source')
    return render(request, 'myapp/quiz/main_goal.html')

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
        return redirect('financial_situation')
    return render(request, 'myapp/quiz/job_challenges.html')

def financial_situation(request):
    if request.method == 'POST':
        request.session['financial_situation'] = request.POST.get('financial_situation')
        return redirect('annual_income_goal')
    return render(request, 'myapp/quiz/financial_situation.html')

def annual_income_goal(request):
    if request.method == 'POST':
        request.session['annual_income_goal'] = request.POST.get('annual_income_goal')
        return redirect('control_work_hours')
    return render(request, 'myapp/quiz/annual_income_goal.html')

def control_work_hours(request):
    if request.method == 'POST':
        request.session['control_work_hours'] = request.POST.get('control_work_hours')
        return redirect('routine_work')
    return render(request, 'myapp/quiz/control_work_hours.html')

def routine_work(request):
    if request.method == 'POST':
        request.session['routine_work'] = request.POST.get('routine_work')
        return redirect('time_saved_use')
    return render(request, 'myapp/quiz/routine_work.html')

def time_saved_use(request):
    if request.method == 'POST':
        request.session['time_saved_use'] = request.POST.get('time_saved_use')
        return redirect('job_interest_match')
    return render(request, 'myapp/quiz/time_saved_use.html')

def job_interest_match(request):
    if request.method == 'POST':
        request.session['job_interest_match'] = request.POST.get('job_interest_match')
        return redirect('digital_business_knowledge')
    return render(request, 'myapp/quiz/job_interest_match.html')

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
        request.session['ai_mastery_readiness'] = request.POST.get('ai_mastery_readiness')
        return redirect('focus_ability')
    return render(request, 'myapp/quiz/ai_mastery_readiness.html')

def focus_ability(request):
    if request.method == 'POST':
        request.session['focus_ability'] = request.POST.get('focus_ability')
        return redirect('summary')
    return render(request, 'myapp/quiz/focus_ability.html')

def summary(request):
    gender = request.session.get('gender', 'male').lower()
    age_range = request.session.get('age_range', '35-44')
    age_group = '35' if '35' in age_range else '45'

    # Determine the image path
    image_path = f"myapp/images/quiz/{gender}{age_group}.png"

    context = {
        'gender': gender,
        'age_range': age_range,
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

def results(request):
    context = {
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
        'job_interest_match': request.session.get('job_interest_match'),
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
        'special_goal': request.session.get('special_goal'),
        'time_to_achieve_goal': request.session.get('time_to_achieve_goal'),
        'email': request.session.get('email'),
        'receive_offers': request.session.get('receive_offers'),
    }
    return render(request, 'myapp/quiz/results.html', context)
