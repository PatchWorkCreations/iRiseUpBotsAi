# customadmin/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='custom_dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
]
