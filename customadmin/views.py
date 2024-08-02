# customadmin/views.py
from django.shortcuts import render, get_object_or_404
from myapp.models import Course

def dashboard(request):
    courses = Course.objects.all()
    return render(request, 'customadmin/dashboard.html', {'courses': courses})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'customadmin/course_list.html', {'courses': courses})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'customadmin/course_detail.html', {'course': course})


# customadmin/views.py
from django.shortcuts import render, redirect
from .forms import CourseForm
from myapp.models import Course

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'customadmin/add_course.html', {'form': form})
