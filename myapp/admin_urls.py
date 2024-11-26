# myapp/admin_urls.py
from django.urls import path
from . import views

app_name = 'custom_admin'  # Updated namespace to 'custom_admin'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('renewals/', views.renewal_dashboard, name='renewals'),
    path('renewals/process/', views.process_renewals, name='process_renewals'),
]
