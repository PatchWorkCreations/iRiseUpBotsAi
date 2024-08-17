from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default="Default description")
    image = models.ImageField(upload_to='course/', default='myapp/images/course/favicon.png')
    units = models.IntegerField()
    hours = models.FloatField()

    def __str__(self):
        return self.title

class SubCourse(models.Model):
    parent_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sub_courses')
    title = models.CharField(max_length=200)
    description = models.TextField(default="Default description")
    units = models.IntegerField()
    hours = models.FloatField()

class Lesson(models.Model):
    parent_sub_course = models.ForeignKey(SubCourse, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    content = models.TextField()

from django.utils import timezone

class UserCourseAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)
    expiration_date = models.DateTimeField(null=True, blank=True)  # Track when access expires

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    def has_expired(self):
        return timezone.now() > self.expiration_date

class UserSubCourseAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_course = models.ForeignKey(SubCourse, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.sub_course.title}"

class QuizResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    gender = models.CharField(max_length=10)
    age_range = models.CharField(max_length=10)
    main_goal = models.CharField(max_length=50)
    income_source = models.CharField(max_length=50)
    work_schedule = models.CharField(max_length=50)
    job_challenges = models.TextField()
    financial_situation = models.CharField(max_length=50)
    annual_income_goal = models.CharField(max_length=50)
    control_work_hours = models.CharField(max_length=10)
    enjoy_routine_job = models.CharField(max_length=10)
    time_saved_use = models.CharField(max_length=50)
    job_interest_match = models.CharField(max_length=10)
    digital_business_knowledge = models.CharField(max_length=50)
    side_hustle_experience = models.CharField(max_length=50)
    learning_new_skills = models.CharField(max_length=10)
    ai_tools_familiarity = models.TextField()
    content_writing_knowledge = models.CharField(max_length=50)
    digital_marketing_knowledge = models.CharField(max_length=50)
    ai_income_boost_awareness = models.CharField(max_length=50)
    fields_interest = models.TextField()
    ai_mastery_readiness = models.CharField(max_length=50)
    focus_ability = models.CharField(max_length=50)
    special_goal = models.CharField(max_length=50)
    time_to_achieve_goal = models.CharField(max_length=50)
    email = models.EmailField()
    receive_offers = models.BooleanField(default=False)

from django.db import models

class EmailCollection(models.Model):
    email = models.EmailField(unique=True)
    receive_offers = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Delayed', 'Delayed')], default='Delayed')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    first_login_completed = models.BooleanField(default=False)  # New field to track first login completion

    def __str__(self):
        return self.email
    
    

from django.db import migrations, models
from django.utils.crypto import get_random_string

def assign_users_based_on_email(apps, schema_editor):
    QuizResponse = apps.get_model('myapp', 'QuizResponse')
    User = apps.get_model('auth', 'User')

    for quiz in QuizResponse.objects.all():
        if not quiz.user_id:  # Only assign if there's no existing user
            email = quiz.email
            user = User.objects.filter(email=email).first()
            if not user:
                # Create a new user with this email
                username = f'user_{get_random_string(8)}'
                user = User.objects.create_user(username=username, password='temporary', email=email)
            quiz.user = user
            quiz.save()

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_emailcollection_payment_status_emailcollection_user'),  # Replace with your previous migration name
    ]

    operations = [
        migrations.AddField(
            model_name='quizresponse',
            name='user',
            field=models.ForeignKey(null=True, on_delete=models.CASCADE, to='auth.User'),
        ),
        migrations.RunPython(assign_users_based_on_email),
        migrations.AlterField(
            model_name='quizresponse',
            name='user',
            field=models.ForeignKey(on_delete=models.CASCADE, to='auth.User'),
        ),
    ]
