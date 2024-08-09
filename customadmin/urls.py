from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('sub_courses/add/', views.add_sub_course, name='add_sub_course'),
    path('sub_courses/<int:sub_course_id>/edit/', views.edit_sub_course, name='edit_sub_course'),
    path('lessons/add/', views.add_lesson, name='add_lesson'),
    path('lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('login/', views.CustomLoginView.as_view(), name='custom_login'),
    path('logout/', views.CustomLogoutView.as_view(), name='custom_logout'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),

]
