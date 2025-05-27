from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, timedelta

class AIIntegrationAccount(models.Model):
    PLAN_CHOICES = [
        ('base', 'Base'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ai_account')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='base')
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
        'myapp.UserIntegrationBot',  # replace 'yourapp' with your actual app name where UserIntegrationBot lives
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
