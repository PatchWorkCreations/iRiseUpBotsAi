from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, timedelta
from pytz import common_timezones

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    remind_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.user.username} at {self.remind_at}"


class AIUserSubscription(models.Model):
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro Monthly'),
        ('one-year', 'One-Year Access')
    ]

    LANGUAGE_CHOICES = [
        ('en-US', 'English'),
        ('ja-JP', 'Japanese'),
        ('es-ES', 'Spanish'),
        ('fr-FR', 'French'),
        ('de-DE', 'German'),
        ('it-IT', 'Italian'),
        ('pt-PT', 'Portuguese (Portugal)'),
        ('pt-BR', 'Portuguese (Brazil)'),
        ('ru-RU', 'Russian'),
        ('zh-CN', 'Chinese (Simplified)'),
        ('zh-TW', 'Chinese (Traditional)'),
        ('ko-KR', 'Korean'),
        ('ar-SA', 'Arabic (Saudi Arabia)'),
        ('tr-TR', 'Turkish'),
        ('nl-NL', 'Dutch'),
        ('sv-SE', 'Swedish'),
        ('pl-PL', 'Polish'),
        ('da-DK', 'Danish'),
        ('no-NO', 'Norwegian'),
        ('fi-FI', 'Finnish'),
        ('he-IL', 'Hebrew'),
        ('th-TH', 'Thai'),
        ('hi-IN', 'Hindi'),
        ('cs-CZ', 'Czech'),
        ('ro-RO', 'Romanian'),
        ('hu-HU', 'Hungarian'),
        ('sk-SK', 'Slovak'),
        ('bg-BG', 'Bulgarian'),
        ('uk-UA', 'Ukrainian'),
        ('vi-VN', 'Vietnamese'),
        ('id-ID', 'Indonesian'),
        ('ms-MY', 'Malay'),
        ('sr-RS', 'Serbian'),
        ('hr-HR', 'Croatian'),
        ('el-GR', 'Greek'),
        ('lt-LT', 'Lithuanian'),
        ('lv-LV', 'Latvian'),
        ('et-EE', 'Estonian'),
        ('sl-SI', 'Slovenian'),
        ('is-IS', 'Icelandic'),
        ('sq-AL', 'Albanian'),
        ('mk-MK', 'Macedonian'),
        ('bs-BA', 'Bosnian'),
        ('ca-ES', 'Catalan'),
        ('gl-ES', 'Galician'),
        ('eu-ES', 'Basque'),
        ('hy-AM', 'Armenian'),
        ('fa-IR', 'Persian'),
        ('sw-KE', 'Swahili'),
        ('ta-IN', 'Tamil'),
        ('te-IN', 'Telugu'),
        ('kn-IN', 'Kannada'),
        ('ml-IN', 'Malayalam'),
        ('mr-IN', 'Marathi'),
        ('pa-IN', 'Punjabi'),
        ('gu-IN', 'Gujarati'),
        ('or-IN', 'Odia'),
        ('as-IN', 'Assamese'),
        ('ne-NP', 'Nepali'),
        ('si-LK', 'Sinhala'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=50, choices=PLAN_CHOICES, default="free")
    start_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    is_auto_renew = models.BooleanField(default=True)  # Auto-renewal flag
    canceled_at = models.DateTimeField(null=True, blank=True)  # Stores when the user cancels

    # New Fields for Chat Tracking
    chat_count = models.IntegerField(default=0)
    chat_last_used = models.DateTimeField(null=True, blank=True)

    # New field for Language Preference
    preferred_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en-US')
    preferred_timezone = models.CharField(max_length=50, choices=[(tz, tz) for tz in common_timezones], default="UTC")


    HEARD_FROM_CHOICES = [
        ('social_media', 'Social Media'),
        ('friend', 'Friend/Referral'),
        ('search', 'Search Engine'),
        ('event', 'Event/Expo'),
        ('other', 'Other'),
    ]

    heard_about_us = models.CharField(
        max_length=50,
        choices=HEARD_FROM_CHOICES,
        default='other',
        verbose_name="How did you hear about us?"
    )



    def save(self, *args, **kwargs):
        """ Ensure expiration_date is correctly set for Pro and One-Year plans. """
        if not self.start_date:  # If start_date is None, assign now()
            self.start_date = now()

        if self.plan == "pro":
            self.expiration_date = self.start_date + timedelta(days=30)
        elif self.plan == "one-year":
            self.expiration_date = self.start_date + timedelta(days=365)
        elif self.plan == "free":
            self.expiration_date = None  # Free plan never expires

        super().save(*args, **kwargs)

    @property
    def is_active(self):
        """ Ensure subscription is active only if expiration_date is in the future OR if it's Free. """
        if self.plan == "free":
            return True  # Free plan never expires
        return self.expiration_date is not None and self.expiration_date > now()

    @property
    def days_remaining(self):
        """ Calculate remaining days until expiration. """
        if self.expiration_date:
            remaining = (self.expiration_date - now()).days
            return max(remaining, 0)  # Prevent negative values
        return 0

    def reset_chat_count_if_needed(self):
        """ Reset chat count if 45 minutes have passed since last use. """
        if self.chat_last_used and now() > self.chat_last_used + timedelta(minutes=45):
            self.chat_count = 0
            self.chat_last_used = now()
            self.save()


    def increment_chat_count(self):
        """ Increment chat count and update last used timestamp. """
        self.chat_count += 1
        self.chat_last_used = now()
        self.save()

    def has_reached_chat_limit(self):
        """ Check if user has exceeded their daily chat limit. """
        self.reset_chat_count_if_needed()

        if self.plan == "free" and self.chat_count >= 20:
            return True
        elif self.plan == "pro" or self.plan == "one-year":
            return False  # Unlimited for paid users

        return False

    def __str__(self):
        status = "Active" if self.is_active else "Expired"
        return f"{self.user.username} - {self.plan} ({status}, {self.days_remaining} days left)"




class SquareCustomer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Support multiple cards
    customer_id = models.CharField(max_length=255, unique=True)
    card_id = models.CharField(max_length=255, unique=True)
    card_brand = models.CharField(max_length=50, blank=True, null=True)  # e.g., Visa, MasterCard
    last_4 = models.CharField(max_length=4, blank=True, null=True)  # Last 4 digits of the card

    def __str__(self):
        return f"{self.user.username} - {self.card_id} ({self.card_brand} ****{self.last_4})"


from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")
    ai_bot = models.CharField(max_length=50)  # e.g., 'Nexara', 'Thrive'
    title = models.CharField(max_length=255, blank=True, null=True)  # AI-generated title
    messages = models.JSONField(default=list)  # Stores chat messages
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # ✅ If no title exists, generate a title based on the first message
        if not self.title and self.messages:
            first_message = self.messages[0].get("content", "New Chat")
            self.title = first_message[:50]  # Limit title length

        super().save(*args, **kwargs)

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from cloudinary.models import CloudinaryField

class AIBot(models.Model):
    AI_TYPE_CHOICES = [
        ('text', 'Text-Based AI'),
        ('image', 'Image Generator AI'),
    ]

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)
    specialty = models.TextField(help_text="What this AI specializes in.")
    description = models.TextField(help_text="Brief description of this AI.")
    bio = models.TextField(help_text="Brief info of this AI.", blank=True, null=True)
    ai_type = models.CharField(max_length=10, choices=AI_TYPE_CHOICES, default="text")
    image = CloudinaryField(
        'image',
        folder='iriseup/ai/icon',
        blank=True,
        null=True
    )
    
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=False, help_text="If true, other users can see and clone this bot.")
    is_favorite = models.BooleanField(default=False)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='custom_bots',
        null=True,
        blank=True,
        help_text="The user who created this bot. Null for admin/system bots."
    )

    cloned_from = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clones',
        help_text="If this bot was cloned, reference the original bot here."
    )

    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_prompt(self):
        return f"""
        You are {self.name}, a specialized AI in {self.specialty}.

        {self.description}

        Stick to your expertise, but stay flexible to the user's needs.
        If you're not sure what they mean, kindly ask questions.
        """

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while AIBot.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @classmethod
    def get_active_bots(cls):
        return cls.objects.filter(is_active=True)

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        visibility = "Public" if self.is_public else "Private"
        return f"{self.name} ({status}, {visibility})"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bot = models.ForeignKey(AIBot, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'bot')

    def __str__(self):
        return f"{self.user.username} ❤️ {self.bot.name}"


from django.db import models
from django.contrib.auth.models import User
import openai

class AIChatSession(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ai_chats")
    ai_bot = models.ForeignKey("AIBot", on_delete=models.CASCADE)  # AI bot used
    title = models.CharField(max_length=255, blank=True, null=True)  # AI-generated or user-renamed title
    messages = models.JSONField(default=list)  # ✅ Store chat messages
    created_at = models.DateTimeField(auto_now_add=True)  # When chat started
    last_updated = models.DateTimeField(auto_now=True)  # When chat was last modified
    session_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")  # ✅ Track chat session status
    manually_renamed = models.BooleanField(default=False)  # ✅ Tracks if user manually renamed the chat

    def generate_chat_title(self, force_update=False):
        """Use AI to generate a meaningful chat title based on the conversation."""
        if self.manually_renamed:  # ✅ If user renamed it, AI should NOT overwrite it
            return

        messages = self.messages[:5]  # ✅ Consider the first 5 messages for better context
        if not messages:
            return  # No messages yet, skip

        # ✅ Fix: Use "content" instead of "message"
        conversation_text = "\n".join([msg.get("content", "") for msg in messages if msg.get("role") == "user"]).strip()

        if not conversation_text:
            self.title = f"Chat with {self.ai_bot.name}"  # ✅ Default title if no user messages
            return

        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Generate a short, meaningful title (max 6 words) summarizing this conversation."},
                    {"role": "user", "content": conversation_text}
                ]
            )

            generated_title = response.choices[0].message.content.strip()
            if len(generated_title.split()) > 6:  # ✅ Keep it short
                generated_title = f"Chat with {self.ai_bot.name}"

            if force_update or not self.title:  # ✅ Update title dynamically unless manually renamed
                self.title = generated_title
                self.save()

        except Exception as e:
            if not self.title:
                self.title = f"Chat with {self.ai_bot.name}"  # ✅ Fallback title
                self.save()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save first to get the ID

        if not self.manually_renamed and (is_new or not self.title):
            self.generate_chat_title(force_update=True)


    def __str__(self):
        return f"Chat with {self.ai_bot.name} - {self.user.username} ({self.created_at.strftime('%Y-%m-%d')})"


from django.db import models
from django.contrib.auth.models import User

class UserLanguagePreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    language_code = models.CharField(max_length=10, default='en-US')  # OpenAI-style language code

    def __str__(self):
        return f"{self.user.username} - {self.language_code}"


from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class AIChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ai_id = models.CharField(max_length=50)  
    title = models.CharField(max_length=255, default="Untitled Chat")  
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.ai_id} - {self.title}"

class AIMessage(models.Model):
    chat = models.ForeignKey(AIChat, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=10, choices=[("user", "User"), ("bot", "Bot")])
    text = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.sender} - {self.chat.title} - {self.timestamp.strftime('%H:%M')}"




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


from django.utils import timezone
from datetime import timedelta

class UserCourseAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_plan = models.CharField(
        max_length=20,
        choices=[('1-week', '1-week'), ('4-week', '4-week'), ('12-week', '12-week'), ('lifetime', 'lifetime')],
        default='1-week'
    )
    expiration_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    has_paid = models.BooleanField(default=False)
    product_id = models.CharField(max_length=20, null=True, blank=True)  # AI Product ID

    # Constants for the different plans
    PLAN_DURATIONS = {
        '1-week': 7,
        '4-week': 28,
        '12-week': 84,
        'lifetime': 9999999,  # Lifetime plan has no expiration
    }

    PLAN_PRICES = {
        '1-week': 100,
        '4-week': 5690,
        '12-week': 16900,
        'lifetime': 24900,
    }

    # New field to indicate whether grace period is applicable
    grace_period_enabled = models.BooleanField(default=False, blank=True, null=True)
    
    # New field for the user to revert downgrade within the grace period
    original_plan = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.selected_plan}"

    def check_expiration(self):
        """Check if the user’s course access has expired"""
        self.is_active = self.expiration_date > timezone.now()
        self.save()

    def renew(self, plan_type):
        """Renew the user's subscription based on plan type"""
        if plan_type in self.PLAN_DURATIONS:
            self.expiration_date = timezone.now() + timedelta(weeks=self.PLAN_DURATIONS[plan_type])
            self.selected_plan = plan_type
            self.is_active = True
            self.has_paid = True  # Set to True once payment is confirmed
            self.save()

    def change_plan(self, new_plan):
        """
        Handle the plan change. Adjust expiration date based on new plan.
        """
        # If the user is upgrading or changing to a new plan, adjust expiration
        current_plan = self.selected_plan
        current_expiration_date = self.expiration_date
        current_price = self.PLAN_PRICES[current_plan]
        new_price = self.PLAN_PRICES[new_plan]

        # If the new plan is different, apply prorating or refund logic
        if new_plan != current_plan:
            unused_days = max((current_expiration_date - timezone.now()).days, 0)
            plan_duration = self.PLAN_DURATIONS[current_plan]
            daily_rate = current_price / plan_duration  # Calculate daily rate

            # Calculate the unused value of the current plan
            unused_value = unused_days * daily_rate

            # Calculate the adjustment amount (new plan cost minus unused value)
            adjustment_amount = max(new_price - unused_value, 0)

            # Cap the prorated charge to ensure users aren’t overcharged
            adjustment_amount = min(adjustment_amount, new_price * 0.75)

            # Update expiration date based on the new plan
            self.selected_plan = new_plan
            if new_plan == 'lifetime':
                self.expiration_date = timezone.now() + timedelta(days=365 * 100)  # Arbitrary long future date
            else:
                self.expiration_date = timezone.now() + timedelta(weeks=self.PLAN_DURATIONS[new_plan])

            self.has_paid = True  # Mark as paid once the payment is confirmed
            self.save()

            # Store the user's original plan before they change (only if it's not already set)
            if not self.original_plan:
                self.original_plan = current_plan
                self.save()

            return {
                'success': True,
                'new_plan': new_plan,
                'amount_charged': adjustment_amount,
                'message': f'Your unused portion from the previous plan has been credited, and your new plan will expire on {self.expiration_date.strftime("%Y-%m-%d")}.'
            }

        return {'success': False, 'error': 'No change in plan selected'}

    def apply_grace_period_for_downgrade(self, grace_period_days=7):
        """
        Allow users to revert their downgrade within a grace period without incurring additional charges.
        Only applies to new users or users with grace_period_enabled set to True.
        """
        if self.grace_period_enabled and self.selected_plan != 'lifetime' and self.expiration_date > timezone.now():
            remaining_time = self.expiration_date - timezone.now()
            if remaining_time.days <= grace_period_days:
                # Revert the user to their original plan within the grace period.
                self.selected_plan = self.original_plan
                self.expiration_date = timezone.now() + timedelta(weeks=self.PLAN_DURATIONS[self.original_plan])
                self.is_active = True  # Reactivate the user's previous plan
                self.save()

                return {
                    'success': True,
                    'message': f'Your downgrade has been reversed. You have {remaining_time.days} days left on your original plan.'
                }
            else:
                return {
                    'success': False,
                    'message': 'The grace period for reverting your downgrade has passed.'
                }
        return {'success': False, 'message': 'No downgrade to revert.'}



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
    email = models.EmailField(unique=False)
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


from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, timedelta

class AIIntegrationAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ai_account')
    plan = models.ForeignKey(
        'myapp.AIIntegrationSubscriptionPlan',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    storage_used = models.BigIntegerField(default=0)  # in bytes
    storage_limit = models.BigIntegerField(default=100 * 1024 * 1024)  # default: 100MB

    bot_limit = models.IntegerField(default=1)
    doc_page_limit = models.IntegerField(default=50)
    behavior_training_limit = models.IntegerField(default=3)
    api_request_limit = models.IntegerField(default=100)  # Base default

    language_count = models.IntegerField(default=1)
    team_member_limit = models.IntegerField(default=1)

    start_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)

    bots_created = models.IntegerField(default=0)
    documents_uploaded = models.IntegerField(default=0)
    embeddings_generated = models.IntegerField(default=0)  # optional but nice to track
    api_requests_today = models.IntegerField(default=0)
    api_reset_on = models.DateField(auto_now_add=True)

    def is_active(self):
        return not self.expiration_date or self.expiration_date > now()

    def __str__(self):
        return f"{self.user.username} ({self.plan.title()})"

class TeamMember(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_members')
    email = models.EmailField()
    role = models.CharField(max_length=50, default='editor')  # admin/editor/viewer

    invited_on = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} ({'Accepted' if self.accepted else 'Pending'})"


class AddOn(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)  # e.g. 'extra_behavior', 'email_reminder'
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Add-ons"

class UserAddOn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addons')
    addon = models.ForeignKey(AddOn, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    activated_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.addon.name} (x{self.quantity})"


from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

class UserIntegrationBot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='integration_bots')
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, help_text="Short description for this bot")

    # Optional: Pre-made public template from your existing system
    template = models.ForeignKey(
        'myapp.AIbot',  # replace 'yourapp' with your actual app name where UserIntegrationBot lives
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='integrated_user_bots',
        help_text="Pick a template bot to start with"
    )

    # Custom tone or prompt override
    custom_tone = models.TextField(
        blank=True,
        help_text="Describe how this bot should behave or speak (e.g., 'encouraging coach', 'strict mentor')"
    )

    vector_path = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Local path or remote ID where this bot's vector index is stored"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def generate_prompt(self):
        template_prompt = self.template.generate_prompt() if self.template else ""
        tone_instructions = f"\n\nTone Instructions:\n{self.custom_tone}" if self.custom_tone else ""
        return f"{template_prompt}{tone_instructions}".strip()

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    class Meta:
        ordering = ['-created_at']



class TrainingSession(models.Model):
    bot = models.ForeignKey(UserIntegrationBot, on_delete=models.CASCADE, related_name='trainings')
    description = models.TextField()
    source_documents = models.ManyToManyField('Document', blank=True)  # New field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Training for {self.bot.name} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"



class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_documents')
    bot = models.ForeignKey(UserIntegrationBot, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)

    name = models.CharField(max_length=200)
    file = models.FileField(upload_to='ai_docs/')
    page_count = models.IntegerField(default=0)
    last_embedded = models.DateTimeField(auto_now=True)
    vector_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name



class AnalyticsSnapshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analytics')
    bot = models.ForeignKey(UserIntegrationBot, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    total_chats = models.IntegerField(default=0)
    total_users = models.IntegerField(default=0)
    top_questions = models.JSONField(default=list)  # ["How can I...", "Tell me about..."]

    def __str__(self):
        return f"{self.user.username} - {self.date}"



class AIIntegrationSubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('base', 'Base'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    code = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    price_monthly = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    bot_limit = models.IntegerField()
    doc_page_limit = models.IntegerField()
    api_request_limit = models.IntegerField()
    language_count = models.IntegerField()
    team_member_limit = models.IntegerField()
    behavior_training_limit = models.IntegerField()

    white_label = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (${self.price_monthly}/mo)"



# models.py

from django.db import models
from django.contrib.auth.models import User

class QuizQuestion(models.Model):
    question_text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.question_text

class QuizChoice(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='quiz_choices/', null=True, blank=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text

class UserQuizAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(QuizChoice, on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} → {self.question} = {self.selected_choice}"

# NEW MODEL: Optional filler screen
class QuizFillerPage(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='quiz_fillers/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title or f"Filler Page {self.id}"



from django.db import models
from django.contrib.auth.models import User

# Choices for staff roles
POSITION_CHOICES = [
    ('regular', 'Regular Employee'),
    ('intern', 'Intern'),
    ('ojt', 'OJT'),
    ('freelancer', 'Freelancer'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position_type = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='regular'
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_position_type_display()}"

class AttendanceLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position_type = models.CharField(max_length=20, choices=POSITION_CHOICES)
    action = models.CharField(max_length=10)  # "in" or "out"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action.upper()} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


from django.db import models
from django.contrib.auth.models import User

class QRCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='qr_files/', blank=True, null=True)
    
    # Use CloudinaryField for QR image
    image = CloudinaryField('image', folder="qrgen/qr_images/")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class ScanLog(models.Model):
    qr_code = models.ForeignKey(QRCode, on_delete=models.CASCADE)
    scanned_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Scan of {self.qr_code.title} at {self.scanned_at}"
