from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('renewals/', views.renewal_dashboard, name='renewals'),
    path('renewals/process/', views.process_renewals, name='process_renewals'),
    path('renewals/generate-links/', views.generate_renewal_links, name='generate_renewal_links'),
    path('renewals/send-links/', views.send_renewal_links, name='send_renewal_links'),
    path('pro-users/', views.pro_users_list, name='pro_users_list'),  # New URL for Pro Users Page
]
