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


from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(default="Default description")
    image = models.ImageField(upload_to='course/', default='myapp/images/course/favicon.png')
    units = models.IntegerField()
    hours = models.FloatField()
    category = models.CharField(max_length=100, null=True, blank=True)
    order = models.PositiveIntegerField(default=0)  # New field to store the order of the courses
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']  # This ensures courses are always ordered by the 'order' field


class SubCourse(models.Model):
    parent_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sub_courses')
    title = models.CharField(max_length=200)
    description = models.TextField(default="Default description")
    units = models.IntegerField()
    hours = models.FloatField()
    order = models.PositiveIntegerField(default=1)  # Add order field

    class Meta:
        ordering = ['order']  # Order by 'order' field by default


class Lesson(models.Model):
    parent_sub_course = models.ForeignKey(SubCourse, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # Add this line
    content = models.TextField()
    order = models.PositiveIntegerField()
    is_first_lesson = models.BooleanField(default=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order == 1:
            self.is_first_lesson = True
        super(Lesson, self).save(*args, **kwargs)

    def is_unlockable_for_user(self, user):
        """
        Determines if the lesson is unlockable for a given user.
        The first lesson is always unlockable. For subsequent lessons, check if the previous one is completed.
        """
        if self.is_first_lesson:
            return True
        previous_lesson = Lesson.objects.filter(
            parent_sub_course=self.parent_sub_course, order=self.order - 1
        ).first()

        if previous_lesson:
            return UserLessonProgress.objects.filter(
                user=user, lesson=previous_lesson, completed=True
            ).exists()

        return False


from django.db import models
from django.core.validators import MinValueValidator

class ContentBlock(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('paragraph', 'Paragraph'),
        ('image', 'Image'),
        ('header', 'Header'),
        ('task', 'Task'),
        ('question', 'Question'),
        ('multiple_questions', 'Multiple Questions'),
        ('multiple_choice', 'Multiple Choice'),
        ('reflection', 'Reflection'),
        ('course_wrap_up', 'Course Wrap-Up'),
        ('congratulations', 'Congratulations'),
        ('video', 'Video'),  # New content type for videos
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='content_blocks')
    type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES)
    content = models.TextField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)  # Field to store video URLs
    order = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)
    
    # Only used for 'multiple_choice' block type
    question = models.TextField(null=True, blank=True)
    correct_answer = models.CharField(max_length=200, null=True, blank=True)
    options = models.JSONField(null=True, blank=True, default=list)  # Store options as a list in JSON format
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.lesson.title} (Order: {self.order})"

    class Meta:
        ordering = ['order']


from django.db import models
from django.contrib.auth.models import User

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Nullable for pre-existing records
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)  # Nullable
    question_type = models.CharField(max_length=50, null=True, blank=True)  # Nullable
    question_content = models.TextField(null=True, blank=True)  # Nullable
    user_answer = models.TextField(null=True, blank=True)  # Nullable
    correct_answer = models.TextField(null=True, blank=True)  # Nullable
    is_correct = models.BooleanField(default=False)
    answered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user.username if self.user else 'Anonymous'} - Correct: {self.is_correct}"


class UserLessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, db_index=True)
    completed = models.BooleanField(default=False, db_index=True)
    completed_on = models.DateTimeField(null=True, blank=True)


    def complete_lesson(self):
        self.completed = True
        self.completed_on = timezone.now()
        self.save()
        self.update_sub_course_progress()

    @staticmethod
    def unlock_next_lesson(user, lesson):
        # Mark the current lesson as completed
        user_progress, created = UserLessonProgress.objects.get_or_create(user=user, lesson=lesson)
        if not user_progress.completed:
            user_progress.complete_lesson()

        # Unlock the next lesson
        next_lesson = Lesson.objects.filter(
            parent_sub_course=lesson.parent_sub_course, order=lesson.order + 1
        ).first()

        if next_lesson:
            return next_lesson.is_unlockable_for_user(user)
        return False


    def update_sub_course_progress(self):
        total_lessons = self.lesson.parent_sub_course.lessons.count()
        completed_lessons = UserLessonProgress.objects.filter(
            user=self.user, lesson__parent_sub_course=self.lesson.parent_sub_course, completed=True
        ).count()

        if total_lessons > 0:
            progress = (completed_lessons / total_lessons) * 100
            UserSubCourseAccess.objects.update_or_create(
                user=self.user, sub_course=self.lesson.parent_sub_course,
                defaults={'progress': progress}
            )


    def is_locked(self):
        """
        Determine if the lesson is locked.
        A lesson is locked if its previous lesson has not been completed.
        """
        previous_lesson = Lesson.objects.filter(
            parent_sub_course=self.lesson.parent_sub_course,
            id__lt=self.lesson.id  # id less than current lesson id
        ).last()  # Fetch the immediately previous lesson
        if previous_lesson:
            previous_progress = UserLessonProgress.objects.filter(
                user=self.user, lesson=previous_lesson, completed=True).exists()
            return not previous_progress  # Locked if the previous lesson is not completed
        return False  # The first lesson is never locked


from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class UserCourseAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    progress = models.FloatField(default=0.0)
    expiration_date = models.DateTimeField(null=True, blank=True)
    renewal_date = models.DateTimeField(null=True, blank=True)  # For scheduling renewal
    renewal_task_id = models.CharField(max_length=255, null=True, blank=True)  # Task ID for the scheduled charge
    selected_plan = models.CharField(max_length=20, null=True, blank=True)
    is_saved = models.BooleanField(default=False, null=True, blank=True)  # Allow nullable values
    is_favorite = models.BooleanField(default=False, null=True, blank=True)  # Allow nullable values


    def __str__(self):
        return f"{self.user.username} - {self.course.title if self.course else 'No course'}"

    def has_expired(self):
        return self.expiration_date is not None and timezone.now() > self.expiration_date

    def update_progress(self):
        """Calculate and update the progress of the entire course based on sub-course completion."""
        total_sub_courses = self.course.sub_courses.count()
        completed_sub_courses = UserSubCourseAccess.objects.filter(
            user=self.user, sub_course__parent_course=self.course, progress=100.0
        ).count()

        if total_sub_courses > 0:
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
        """Calculate and update the progress of the sub-course based on lesson completion."""
        total_lessons = self.sub_course.lessons.count()
        completed_lessons = UserLessonProgress.objects.filter(
            user=self.user, lesson__parent_sub_course=self.sub_course, completed=True
        ).count()

        if total_lessons > 0:
            # Calculate the percentage of progress
            self.progress = (completed_lessons / total_lessons) * 100
            self.save()

            # Print debugging information to verify the calculation
            print(f"Sub-course: {self.sub_course.title}")
            print(f"Total lessons: {total_lessons}, Completed lessons: {completed_lessons}")
            print(f"Calculated Progress: {self.progress}%")
            
            # Update the overall course progress
            self.update_course_progress()


    def update_course_progress(self):
        """Update the course progress after updating the sub-course progress."""
        user_course_access = UserCourseAccess.objects.get(
            user=self.user, course=self.sub_course.parent_course
        )
        user_course_access.update_progress()  # Call the course progress update function


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
    description = models.TextField(blank=True, null=True)  # Add this line
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


from django.db import models
from django.contrib.auth.models import User

class ForumCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class ForumPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='posts', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='post_dislikes', blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def total_comments(self):
        return self.forum_comments.count()

class ForumComment(models.Model):
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='forum_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255, default='female_avatar1')
    bio = models.TextField(blank=True, null=True)
    
    def get_avatar_choices(self):
        quiz_response = QuizResponse.objects.filter(user=self.user).first()
        if quiz_response and quiz_response.gender == 'Male':
            return [
                ('male_avatar1', 'Male Avatar 1'),
                ('male_avatar2', 'Male Avatar 2'),
                ('male_avatar3', 'Male Avatar 3')
            ]
        elif quiz_response and quiz_response.gender == 'Female':
            return [
                ('female_avatar1', 'Female Avatar 1'),
                ('female_avatar2', 'Female Avatar 2'),
                ('female_avatar3', 'Female Avatar 3'),
                ('female_avatar4', 'Female Avatar 4'),
                ('female_avatar5', 'Female Avatar 5'),
                ('female_avatar7', 'Female Avatar 7'),
                ('female_avatar8', 'Female Avatar 8'),
                ('female_avatar9', 'Female Avatar 9')
            ]
        else:
            return [
                ('neutral_avatar1', 'Neutral Avatar 1'),
                ('neutral_avatar2', 'Neutral Avatar 2'),
                ('neutral_avatar3', 'Neutral Avatar 3')
            ]


    def __str__(self):
        return self.user.username
    

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50)
    subscription_id = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)  # Ensure it's nullable if this is what you want
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan} subscription"


from django.db import models
from django.utils import timezone

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('success', 'Success'),
        ('pending', 'Pending'),
        ('error', 'Error'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', db_index=True)
    transaction_date = models.DateTimeField(default=timezone.now, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    subscription_type = models.CharField(max_length=100)
    error_logs = models.TextField(blank=True, null=True)  # To capture error details if any
    recurring = models.BooleanField(default=False)  # If it's recurring billing
    next_billing_date = models.DateTimeField(blank=True, null=True)  # For recurring payments

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type} - {self.status}"


# models.py
from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(unique=True, null=True)  # Allows NULL values for email
    subscribed_on = models.DateTimeField(auto_now_add=True)  # Timestamp of subscription

    def __str__(self):
        return self.email if self.email else "No Email"  # Handle case where email is NULL


from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User  # Import User model for the author field
from django.urls import reverse



from django.db import models
from django.contrib.auth.models import User  # Assuming you have this imported

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateField()
    image = models.ImageField(blank=True, null=True, upload_to='blog_images/')
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField(Category, related_name='blogs')
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    def get_absolute_url(self):
        return reverse('blog_detail', args=[self.slug])

    def read_time(self):
        word_count = len(self.content.split())
        return f"{word_count // 200} min read"

    def __str__(self):
        return self.title


class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
