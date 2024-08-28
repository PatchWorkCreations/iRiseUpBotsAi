from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class SquareCustomer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=255, unique=True)
    card_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.customer_id}"


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

class UserLessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title} (Completed: {self.completed})"


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class UserCourseAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)  # Allow null values
    progress = models.FloatField(default=0.0)
    expiration_date = models.DateTimeField(null=True, blank=True)
    renewal_date = models.DateTimeField(null=True, blank=True)  # Added for renewal scheduling

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

    def has_expired(self):
        return self.expiration_date is not None and timezone.now() > self.expiration_date

    def update_progress(self):
        # Automatically calculate progress based on completed sub-courses or lessons
        total_sub_courses = self.course.sub_courses.count()
        if total_sub_courses > 0:
            completed_sub_courses = UserSubCourseAccess.objects.filter(
                user=self.user, sub_course__parent_course=self.course, progress=100.0).count()
            self.progress = (completed_sub_courses / total_sub_courses) * 100
            self.save()

    def set_renewal_date(self, plan_duration):
        """Sets the renewal date based on the plan duration in weeks."""
        if plan_duration:
            self.renewal_date = timezone.now() + timedelta(weeks=plan_duration)
            self.save()


class UserSubCourseAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sub_course = models.ForeignKey(SubCourse, on_delete=models.CASCADE)
    progress = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.sub_course.title}"

    def update_progress(self):
        # Automatically calculate progress based on completed lessons
        total_lessons = self.sub_course.lessons.count()
        if total_lessons > 0:
            completed_lessons = UserLessonProgress.objects.filter(user=self.user, lesson__parent_sub_course=self.sub_course, completed=True).count()
            self.progress = (completed_lessons / total_lessons) * 100
            self.save()


from django.contrib.auth.models import User
from django.db import models

class QuizResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Add this line
    gender = models.CharField(max_length=50)
    age_range = models.CharField(max_length=50)
    main_goal = models.CharField(max_length=50)
    income_source = models.CharField(max_length=50)
    work_schedule = models.CharField(max_length=50)
    job_challenges = models.TextField()
    financial_situation = models.CharField(max_length=50)
    annual_income_goal = models.CharField(max_length=50)
    control_work_hours = models.CharField(max_length=50)
    enjoy_routine_job = models.CharField(max_length=50)
    time_saved_use = models.CharField(max_length=50)
    job_interest_match = models.CharField(max_length=50)
    digital_business_knowledge = models.CharField(max_length=50)
    side_hustle_experience = models.CharField(max_length=50)
    learning_new_skills = models.CharField(max_length=50)
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


class KnowledgeBaseCategory(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True)

    def __str__(self):
        return self.title

class KnowledgeBaseSubCategory(models.Model):
    category = models.ForeignKey(KnowledgeBaseCategory, related_name='subcategories', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='subcategory_icons/', blank=True, null=True)

    def __str__(self):
        return f"{self.category.title} - {self.title}"

class KnowledgeBaseArticle(models.Model):
    subcategory = models.ForeignKey(KnowledgeBaseSubCategory, related_name='articles', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    date_modified = models.DateField(auto_now=True)
    is_popular = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    


class EmailCollection(models.Model):
    email = models.EmailField(unique=False, null=False, blank=False)  # Enforcing non-null, non-blank values
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='email_collection')
    receive_offers = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Delayed', 'Delayed')], default='Delayed')
    created_at = models.DateTimeField(auto_now_add=True)
    first_login_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.email



