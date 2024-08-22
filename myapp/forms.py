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


from .models import KnowledgeBaseCategory, KnowledgeBaseSubCategory, KnowledgeBaseArticle

class KnowledgeBaseCategoryForm(forms.ModelForm):
    class Meta:
        model = KnowledgeBaseCategory
        fields = ['title', 'description', 'icon']


class KnowledgeBaseSubCategoryForm(forms.ModelForm):
    class Meta:
        model = KnowledgeBaseSubCategory
        fields = ['category', 'title', 'description']

class KnowledgeBaseArticleForm(forms.ModelForm):
    class Meta:
        model = KnowledgeBaseArticle
        fields = ['subcategory', 'title', 'content', 'is_popular']



from django import forms

class SubmitRequestForm(forms.Form):
    REQUEST_TYPES = [
        ('subscription', 'Subscription'),
        ('payments', 'Payments'),
        ('sign_in', 'Sign-In Help'),
        ('other', 'Other'),
    ]

    requester = forms.CharField(max_length=100, required=True)
    subject = forms.CharField(max_length=100, required=True)
    query_type = forms.ChoiceField(choices=REQUEST_TYPES, required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)
    attachment = forms.FileField(required=False)
    email = forms.EmailField(required=True)

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomPasswordResetForm(forms.Form):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("The two password fields must match.")
        
        if len(password1) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        
        return cleaned_data
