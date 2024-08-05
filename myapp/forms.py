# myapp/forms.py
from django import forms
from .models import Course, SubCourse, Lesson

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'image', 'units', 'hours']

class SubCourseForm(forms.ModelForm):
    class Meta:
        model = SubCourse
        fields = ['parent_course', 'title', 'description', 'units', 'hours']

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label='Select a CSV file',
        help_text='Max. 10 megabytes'
    )
