from django.utils import timezone
from django.core.mail import send_mail
from .models import Reminder
import logging

logger = logging.getLogger(__name__)

def send_due_reminders():
    now_utc = timezone.now()
    window_start = now_utc
    window_end = now_utc + timezone.timedelta(minutes=1)

    reminders = Reminder.objects.filter(remind_at__gte=window_start, remind_at__lt=window_end)

    logger.info(f"🕵️ Checking reminders between {window_start} and {window_end}")
    logger.info(f"🔍 Found {reminders.count()} reminders")

    for reminder in reminders:
        logger.info(f"📬 Sending reminder to {reminder.user.email}: {reminder.message}")
        send_mail(
            subject="⏰ Your AI Reminder",
            message=f"Hi {reminder.user.username},\n\nJust a reminder: {reminder.message}\n\n- iRiseUp.AI",
            from_email="iRiseUp.AI <iriseupgroupofcompanies@gmail.com>",
            recipient_list=[reminder.user.email],
        )
