from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import send_due_reminders

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_due_reminders, 'interval', minutes=1)
    print("✅ APScheduler started...")  # ← Add this line
    scheduler.start()
