from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from myapp.forms import CourseForm, SubCourseForm, LessonForm
from myapp.models import Course, SubCourse, Lesson
from django.template.loader import render_to_string
from django.http import JsonResponse
import json
import os
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy


def dashboard(request):
    courses = Course.objects.all()
    return render(request, 'customadmin/dashboard.html', {'courses': courses})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'customadmin/course_list.html', {'courses': courses})

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    sub_courses = course.sub_courses.all()
    return render(request, 'myapp/course_detail.html', {'course': course, 'sub_courses': sub_courses})

def add_course(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST, request.FILES)
        if course_form.is_valid():
            course = course_form.save()
            generate_course_html(course)
            return redirect('course_list')
    else:
        course_form = CourseForm()
    return render(request, 'customadmin/add_course.html', {'course_form': course_form})

def generate_course_html(course):
    context = {'course': course}
    html_content = render_to_string('myapp/course_templates/base_course_template.html', context)
    file_path = os.path.join('myapp/templates/myapp/generated_courses', f'{course.title}.html')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(html_content)

def add_sub_course(request):
    if request.method == 'POST':
        form = SubCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = SubCourseForm()
    return render(request, 'customadmin/add_sub_course.html', {'form': form})

def edit_sub_course(request, sub_course_id):
    sub_course = get_object_or_404(SubCourse, id=sub_course_id)
    if request.method == 'POST':
        form = SubCourseForm(request.POST, instance=sub_course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=sub_course.parent_course.id)
    else:
        form = SubCourseForm(instance=sub_course)
    return render(request, 'customadmin/edit_sub_course.html', {'form': form, 'sub_course': sub_course})

def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            sub_course_id = request.POST.get('parent_sub_course')
            if sub_course_id:
                lesson.parent_sub_course = get_object_or_404(SubCourse, id=sub_course_id)
                lesson.save()
                return redirect('course_list')  # Change this to the appropriate redirect URL
            else:
                form.add_error('parent_sub_course', 'This field is required.')
    else:
        form = LessonForm()
    sub_courses = SubCourse.objects.all()
    return render(request, 'customadmin/add_lesson.html', {'form': form, 'sub_courses': sub_courses})


def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if request.method == 'POST':
        lesson.description = request.POST.get('description', '')
        content_blocks = []
        for idx in range(int(request.POST.get('block_count', '0'))):
            block_type = request.POST.get(f'block_type_{idx}')
            if block_type == 'paragraph':
                content = request.POST.get(f'content_{idx}', '')
                content_blocks.append({'type': 'paragraph', 'content': content})
            elif block_type == 'image':
                image = request.FILES.get(f'image_{idx}')
                if image:
                    # Handle image upload and get the URL
                    image_url = handle_uploaded_file(image)
                    content_blocks.append({'type': 'image', 'content': image_url})
            elif block_type == 'header':
                content = request.POST.get(f'content_{idx}', '')
                content_blocks.append({'type': 'header', 'content': content})
        
        lesson.content = json.dumps(content_blocks)
        lesson.save()
        return redirect('course_detail', lesson.parent_sub_course.parent_course.id)
    
    try:
        content_blocks = json.loads(lesson.content)
    except json.JSONDecodeError:
        content_blocks = []
    
    context = {
        'lesson': lesson,
        'content_blocks': content_blocks,
        'block_count': range(len(content_blocks)),  # Pass the range to the template
    }
    return render(request, 'customadmin/edit_lesson.html', context)

def handle_uploaded_file(f):
    # Save the file to the appropriate location and return its URL
    file_path = os.path.join('media', 'lesson_images', f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    sub_courses = course.sub_courses.all()
    return render(request, 'customadmin/edit_course.html', {'course': course, 'form': form, 'sub_courses': sub_courses})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        # Delete the generated HTML file
        file_path = os.path.join(settings.BASE_DIR, 'myapp/templates/myapp/generated_courses', f'{course.title}.html')
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete the course
        course.delete()
        return redirect('course_list')
    return render(request, 'customadmin/confirm_delete.html', {'course': course})

class CustomLoginView(LoginView):
    template_name = 'customadmin/login.html'

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('custom_dashboard')

# customadmin/views.py
import os
from django.conf import settings

def handle_uploaded_file(f):
    # Define the directory path relative to MEDIA_ROOT
    directory = os.path.join(settings.MEDIA_ROOT, 'lesson_images')
    
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Define the full file path
    file_path = os.path.join(directory, f.name)
    
    # Save the file to the appropriate location
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    # Return the relative URL path
    return os.path.join(settings.MEDIA_URL, 'lesson_images', f.name)


from django.shortcuts import render, redirect
from django.contrib import messages
from myapp.forms import CSVUploadForm
from myapp.models import Course, SubCourse, Lesson

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'The file is not CSV type')
                return redirect('upload_csv')
            try:
                data = csv_file.read().decode('utf-8')
                reader = csv.DictReader(data.splitlines())
                for row in reader:
                    if 'course' in request.path:
                        Course.objects.create(
                            title=row['title'],
                            description=row['description'],
                            units=row['units'],
                            hours=row['hours']
                        )
                    elif 'sub_course' in request.path:
                        SubCourse.objects.create(
                            parent_course=Course.objects.get(title=row['parent_course']),
                            title=row['title'],
                            description=row['description'],
                            units=row['units'],
                            hours=row['hours']
                        )
                    elif 'lesson' in request.path:
                        Lesson.objects.create(
                            parent_sub_course=SubCourse.objects.get(title=row['parent_sub_course']),
                            title=row['title'],
                            content=row['content']
                        )
                messages.success(request, 'CSV file processed successfully')
                return redirect('some_view')
            except Exception as e:
                messages.error(request, f'Error processing CSV file: {e}')
                return redirect('upload_csv')
    else:
        form = CSVUploadForm()

    return render(request, 'upload_csv.html', {'form': form})
