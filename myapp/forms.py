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
    
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class CustomPasswordChangeForm(PasswordChangeForm):
    username = forms.CharField(
        label="Username",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'old_password', 'new_password1', 'new_password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.user.username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


from django import forms
from django.contrib.auth.models import User
from .models import EmailCollection

class UpdateProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your username'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(username=self.instance.username).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Apply space validation only if the username is new or being changed
        if self.instance.pk is None or self.instance.username != username:
            if ' ' in username:
                raise forms.ValidationError("Usernames cannot contain spaces.")

        # Ensure the new username isn't already taken
        if User.objects.filter(username=username).exclude(email=self.instance.email).exists():
            raise forms.ValidationError('This username is already in use.')

        return username


from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class StandardPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignInForm(forms.Form):
    login_identifier = forms.CharField(
        label="Username or Email",
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username or email'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        required=True
    )

    def clean_login_identifier(self):
        login_identifier = self.cleaned_data.get('login_identifier')
        if ' ' in login_identifier:
            raise ValidationError("Invalid login identifier. Usernames cannot contain spaces.")
        return login_identifier

from django import forms
from .models import ForumPost, ForumComment, ForumCategory

class ForumPostForm(forms.ModelForm):
    anonymous = forms.BooleanField(required=False, label="Post anonymously")

    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'category' , 'anonymous']  # Ensure 'category' is included

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Comment as {}'.format('Anonymous' if not 'user' in locals() else '{{ user.username }}'),
                'rows': 3,  # Adjust the height of the textarea by setting the number of rows
            }),
        }


from django import forms
from .models import ForumPost, ForumCategory

class ForumPostForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100, required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Suggest a new category'})
    )

    class Meta:
        model = ForumPost
        fields = ['title', 'content', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter post title'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Write your content here'})


from django import forms
from .models import UserProfile

class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AvatarForm, self).__init__(*args, **kwargs)
        
        # If user is provided, customize the avatar choices based on the user
        if user:
            self.fields['avatar'].choices = self.instance.get_avatar_choices()



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']  # Only update the bio field

from django import forms
from myapp.models import BlogComment

class BlogCommentForm (forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']  # Adjust fields as necessary
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write your comment here...'}),
        }

