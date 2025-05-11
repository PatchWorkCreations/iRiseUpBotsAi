# myapp/apps.py
from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def start_scheduler():
    if not scheduler.running:
        print("✅ APScheduler started!")
        scheduler.start()

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        start_scheduler()
