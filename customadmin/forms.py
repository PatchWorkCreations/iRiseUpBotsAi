# customadmin/forms.py
from django import forms
from myapp.models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'units', 'hours']
