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

from django.shortcuts import get_object_or_404, redirect

from django.shortcuts import redirect, get_object_or_404

def add_sub_course(request):
    # Fetch the course using course_id from GET parameters
    course_id = request.GET.get('course_id')
    parent_course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        form = SubCourseForm(request.POST)
        if form.is_valid():
            sub_course = form.save(commit=False)
            sub_course.parent_course = parent_course  # Link the new sub-course to the parent course
            sub_course.order = SubCourse.objects.filter(parent_course=parent_course).count() + 1
            sub_course.save()
            return redirect('edit_course', course_id=parent_course.id)
    else:
        form = SubCourseForm()

    return render(request, 'customadmin/add_sub_course.html', {'form': form, 'course': parent_course})


def edit_sub_course(request, sub_course_id):
    sub_course = get_object_or_404(SubCourse, id=sub_course_id)
    if request.method == 'POST':
        form = SubCourseForm(request.POST, instance=sub_course)
        if form.is_valid():
            form.save()
            return redirect('edit_course', course_id=sub_course.parent_course.id)
    else:
        form = SubCourseForm(instance=sub_course)
    return render(request, 'customadmin/edit_sub_course.html', {'form': form, 'sub_course': sub_course})

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

def handle_uploaded_file(file):
    upload_dir = '/Users/Julia/Downloads/braine-package/myapp/static/myapp/images/lesson_images/'
    
    # Ensure the directory exists
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_path = os.path.join(upload_dir, file.name)
    
    # Save the file in the specified directory
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    
    # Return the relative file path for template use
    return f'/static/myapp/images/lesson_images/{file.name}'

def add_lesson(request):
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            sub_course_id = request.POST.get('parent_sub_course')
            if sub_course_id:
                sub_course = get_object_or_404(SubCourse, id=sub_course_id)
                lesson.parent_sub_course = sub_course
                # Assign the next available order for the lesson under the subcourse
                lesson.order = Lesson.objects.filter(parent_sub_course=sub_course).count() + 1
                lesson.save()
                return redirect('edit_course', course_id=sub_course.parent_course.id)  # Redirect to course detail page
            else:
                form.add_error('parent_sub_course', 'This field is required.')
    else:
        form = LessonForm()
    sub_courses = SubCourse.objects.all()
    return render(request, 'customadmin/add_lesson.html', {'form': form, 'sub_courses': sub_courses})


def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':
        # Update the lesson description
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
                    image_url = handle_uploaded_file(image)
                    content_blocks.append({'type': 'image', 'content': image_url})

            elif block_type == 'header':
                content = request.POST.get(f'content_{idx}', '')
                content_blocks.append({'type': 'header', 'content': content})

            elif block_type == 'task':
                task_content = request.POST.get(f'content_{idx}', '')
                content_blocks.append({'type': 'task', 'content': task_content})

            elif block_type == 'question':
                question_content = request.POST.get(f'content_{idx}', '')
                content_blocks.append({'type': 'question', 'content': question_content})

            elif block_type == 'multiple_questions':
                multiple_question_content = request.POST.get(f'content_{idx}', '')
                questions_list = [q.strip() for q in multiple_question_content.split(',')]
                content_blocks.append({'type': 'multiple_questions', 'content': questions_list})

            elif block_type == 'multiple_choice':
                question = request.POST.get(f'question_{idx}', '')
                correct_answer = request.POST.get(f'correct_answer_{idx}', '')
                options = request.POST.getlist(f'option_{idx}[]')
                content_blocks.append({
                    'type': 'multiple_choice',
                    'question': question,
                    'options': options,
                    'correct_answer': correct_answer
                })

        # Save the updated content blocks in JSON format
        lesson.content = json.dumps(content_blocks)
        lesson.save()

        # Redirect back to the course detail page after saving
        return redirect('course_detail', lesson.parent_sub_course.parent_course.id)

    # Load existing content blocks if available
    try:
        content_blocks = json.loads(lesson.content)
    except json.JSONDecodeError:
        content_blocks = []

    context = {
        'lesson': lesson,
        'content_blocks': content_blocks,
        'block_count': len(content_blocks),  # Pass the number of blocks to the template
    }
    return render(request, 'customadmin/edit_lesson.html', context)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import UserAnswer

@csrf_exempt
def process_answer(request, lesson_id, question_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    content_blocks = json.loads(lesson.content)
    
    # Ensure question_id is valid
    if question_id >= len(content_blocks) or question_id < 0:
        return JsonResponse({'error': 'Invalid question ID'}, status=404)
    
    question_block = content_blocks[question_id]

    # Ensure it's a multiple-choice question
    if question_block.get('type') != 'multiple_choice':
        return JsonResponse({'error': 'Question is not a multiple-choice type'}, status=400)

    user_answer = request.POST.get(f'answer_{question_id}', '').strip().lower()
    correct_answer = question_block.get('correct_answer', '').strip().lower()

    is_correct = user_answer == correct_answer

    # Save the user's answer to the database
    UserAnswer.objects.create(
        user=request.user,
        lesson=lesson,
        question_type=question_block.get('type'),
        question_content=question_block.get('question'),
        user_answer=user_answer,
        correct_answer=correct_answer,
        is_correct=is_correct
    )

    # Return the response as JSON
    return JsonResponse({
        'correct': is_correct,
        'correct_answer': correct_answer
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.models import Lesson, ContentBlock

@csrf_exempt
def save_block(request, block_id):
    if request.method == 'POST':
        block_type = request.POST.get('block_type')
        content = request.POST.get('content')
        question = request.POST.get('question')
        correct_answer = request.POST.get('correct_answer')

        # Retrieve or create the block
        block = ContentBlock.objects.get(id=block_id)

        # Update the block data
        block.type = block_type
        block.content = content
        block.question = question
        block.correct_answer = correct_answer
        block.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect

def update_sub_course_order(request, sub_course_id):
    sub_course = get_object_or_404(SubCourse, id=sub_course_id)
    if request.method == 'POST':
        new_order = request.POST.get('order')
        if new_order:
            sub_course.order = int(new_order)
            sub_course.save()
    return redirect('edit_course', course_id=sub_course.parent_course.id)

def update_lesson_order(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        new_order = request.POST.get('order')
        if new_order:
            lesson.order = int(new_order)
            lesson.save()
    return redirect('edit_course', course_id=lesson.parent_sub_course.parent_course.id)


def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('edit_course', course_id=course.id)
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
    next_page = reverse_lazy('dashboard')

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
import csv


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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from myapp.models import EmailCollection

def user_management(request):
    users = User.objects.all()
    email_collections = EmailCollection.objects.all()
    context = {
        'users': users,
        'email_collections': email_collections,
    }
    return render(request, 'customadmin/user_management.html', context)

def send_password_reset(request, user_id):
    user = get_object_or_404(User, id=user_id)
    subject = 'Password Reset Request'
    message = f'Click the link below to reset your password:\n\n{request.build_absolute_uri(reverse("password_reset_confirm", args=[user.id]))}'
    send_mail(subject, message, 'from@example.com', [user.email])
    return redirect('user_management')


# customadmin/views.py


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from myapp.models import EmailCollection, QuizResponse  # Import the QuizResponse model

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from myapp.models import QuizResponse

def view_user_quiz_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    try:
        quiz_response = QuizResponse.objects.get(user=user)
    except QuizResponse.DoesNotExist:
        quiz_response = None  # Handle the case where there's no QuizResponse

    return render(request, 'customadmin/view_user_quiz_details.html', {
        'user': user,
        'quiz_response': quiz_response,
    })


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        # Handle user update logic here
        user.email = request.POST.get('email', user.email)
        user.save()
        return redirect('customadmin_user_management')
    return render(request, 'customadmin/edit_user.html', {'user': user})

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User  # Assuming User is the model you're deleting

def delete_user(request, item_id):
    item = get_object_or_404(User, id=item_id)  # Adjust the model as needed
    if request.method == 'POST':
        item.delete()
        return redirect('user_management')  # Replace with the correct redirect URL
    return render(request, 'customadmin/delete_user.html', {'item': item})


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest

def delete_multiple_users(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        if not user_ids:
            return HttpResponseBadRequest('No users selected')

        User.objects.filter(id__in=user_ids).delete()
        return redirect('user_management')
    return HttpResponseBadRequest('Invalid request method')


from django.shortcuts import render, get_object_or_404, redirect
from myapp.models import KnowledgeBaseCategory, KnowledgeBaseSubCategory, KnowledgeBaseArticle
from myapp.forms import KnowledgeBaseCategoryForm, KnowledgeBaseSubCategoryForm, KnowledgeBaseArticleForm

# Manage Knowledge Base View
def manage_knowledge_base(request):
    categories = KnowledgeBaseCategory.objects.all()
    subcategories = KnowledgeBaseSubCategory.objects.all()
    articles = KnowledgeBaseArticle.objects.all()

    # Debugging prints
    print("Categories:", categories)
    print("Subcategories:", subcategories)
    print("Articles:", articles)

    context = {
        'categories': categories,
        'subcategories': subcategories,
        'articles': articles,
    }
    return render(request, 'customadmin/manage_knowledge_base.html', context)

# Add Category View
def add_category(request):
    if request.method == 'POST':
        form = KnowledgeBaseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_knowledge_base')
    else:
        form = KnowledgeBaseCategoryForm()
    return render(request, 'customadmin/add_category.html', {'form': form})

# Edit Category View
def edit_category(request, id=None):
    category = None
    if id:
        category = get_object_or_404(KnowledgeBaseCategory, id=id)

    if request.method == 'POST':
        form = KnowledgeBaseCategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('manage_knowledge_base')
    else:
        form = KnowledgeBaseCategoryForm(instance=category)

    return render(request, 'customadmin/edit_category.html', {
        'form': form,
        'category': category,
    })

# Add Subcategory View
def add_subcategory(request):
    categories = KnowledgeBaseCategory.objects.all()

    if request.method == 'POST':
        category_id = request.POST['category']
        title = request.POST['title']
        description = request.POST['description']
        icon = request.FILES.get('icon')

        category = get_object_or_404(KnowledgeBaseCategory, id=category_id)
        KnowledgeBaseSubCategory.objects.create(
            category=category,
            title=title,
            description=description,
            icon=icon
        )
        return redirect('manage_knowledge_base')

    return render(request, 'customadmin/add_subcategory.html', {'categories': categories})

# Edit Subcategory View
def edit_subcategory(request, id):
    subcategory = get_object_or_404(KnowledgeBaseSubCategory, id=id)
    if request.method == 'POST':
        form = KnowledgeBaseSubCategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('manage_knowledge_base')
    else:
        form = KnowledgeBaseSubCategoryForm(instance=subcategory)
    return render(request, 'customadmin/edit_subcategory.html', {'form': form})

# Add Article View
def add_article(request):
    subcategories = KnowledgeBaseSubCategory.objects.all()
    if request.method == 'POST':
        form = KnowledgeBaseArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_knowledge_base')
    else:
        form = KnowledgeBaseArticleForm()
    return render(request, 'customadmin/add_article.html', {'form': form, 'subcategories': subcategories})

# Edit Article View

from django.shortcuts import render, get_object_or_404, redirect
from myapp.models import KnowledgeBaseArticle
from myapp.forms import KnowledgeBaseArticleForm
import json

def edit_article(request, id):
    article = get_object_or_404(KnowledgeBaseArticle, id=id)
    
    if request.method == 'POST':
        form = KnowledgeBaseArticleForm(request.POST, instance=article)
        if form.is_valid():
            # Save the basic form data
            article = form.save(commit=False)
            
            # Process the content blocks
            block_count = int(request.POST.get('block_count', 0))
            content_blocks = []
            for i in range(block_count):
                block_type = request.POST.get(f'block_type_{i}')
                if block_type == 'paragraph':
                    content = request.POST.get(f'content_{i}', '')
                    content_blocks.append({'type': 'paragraph', 'content': content})
                elif block_type == 'image':
                    image = request.FILES.get(f'image_{i}')
                    if image:
                        # Handle image upload and get the URL
                        image_url = handle_uploaded_file(image)  # Assuming this is defined elsewhere
                        content_blocks.append({'type': 'image', 'content': image_url})
                elif block_type == 'header':
                    content = request.POST.get(f'content_{i}', '')
                    content_blocks.append({'type': 'header', 'content': content})
            
            # Save the content blocks as JSON in the article's content field
            article.content = json.dumps(content_blocks)
            article.save()

            return redirect('manage_knowledge_base')
    else:
        form = KnowledgeBaseArticleForm(instance=article)

    try:
        content_blocks = json.loads(article.content)  # Assuming content is stored as JSON
    except json.JSONDecodeError:
        content_blocks = []

    context = {
        'form': form,
        'article': article,
        'content_blocks': content_blocks,
    }

    return render(request, 'customadmin/edit_article.html', context)


from django.shortcuts import redirect, get_object_or_404
from myapp.models import KnowledgeBaseCategory, KnowledgeBaseSubCategory, KnowledgeBaseArticle


def delete_category(request, category_id):
    category = get_object_or_404(KnowledgeBaseCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
    return redirect('manage_knowledge_base')

def delete_subcategory(request, id):
    subcategory = get_object_or_404(KnowledgeBaseSubCategory, id=id)
    if request.method == 'POST':
        subcategory.delete()
    return redirect('manage_knowledge_base')

def delete_article(request, article_id):
    article = get_object_or_404(KnowledgeBaseArticle, id=article_id)
    if request.method == 'POST':
        article.delete()
    return redirect('manage_knowledge_base')


import csv
from django.http import HttpResponse, JsonResponse
from myapp.models import Transaction

# View for downloading transactions as a CSV file
def download_transactions_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['User', 'Subscription Type', 'Amount', 'Status', 'Transaction Date', 'Recurring', 'Next Billing Date', 'Error Logs'])

    # Write data rows
    transactions = Transaction.objects.all().values_list(
        'user__email', 'subscription_type', 'amount', 'status', 'created_at', 'recurring', 'next_billing_date', 'error_logs'
    )
    for transaction in transactions:
        writer.writerow(transaction)

    return response


# API view to get transactions data for rendering in HTML
def view_transactions(request):
    status = request.GET.get('status', None)
    if status:
        transactions = Transaction.objects.filter(status=status)
    else:
        transactions = Transaction.objects.all()

    transactions_list = [
        {
            "user": transaction.user.email,
            "subscription_type": transaction.subscription_type,
            "amount": transaction.amount,
            "status": transaction.status,
            "transaction_date": transaction.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "recurring": transaction.recurring,
            "next_billing_date": transaction.next_billing_date.strftime("%Y-%m-%d") if transaction.next_billing_date else None,
            "error_logs": transaction.error_logs,
        }
        for transaction in transactions
    ]

    return JsonResponse({"transactions": transactions_list})


# views.py
# views.py
from django.shortcuts import render
from myapp.models import Transaction

def customadmin_transactions(request):
    # Fetch all transactions from the database
    transactions = Transaction.objects.all()
    
    return render(request, 'customadmin/transactions.html', {'transactions': transactions})


def delete_sub_course(request, sub_course_id):
    sub_course = get_object_or_404(SubCourse, id=sub_course_id)
    if request.method == 'POST':
        sub_course.delete()
        return redirect('edit_course', course_id=sub_course.parent_course.id)
    return render(request, 'customadmin/confirm_delete.html', {'sub_course': sub_course})

def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        lesson.delete()
        return redirect('edit_course', course_id=lesson.parent_sub_course.parent_course.id)
    return render(request, 'customadmin/confirm_delete.html', {'lesson': lesson})
