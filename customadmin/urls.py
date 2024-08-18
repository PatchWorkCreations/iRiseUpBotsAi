from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomLoginView.as_view(), name='custom_login'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Use the function-based view
    path('courses/', views.course_list, name='course_list'),
    path('user-management/', views.user_management, name='user_management'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('sub_courses/add/', views.add_sub_course, name='add_sub_course'),
    path('sub_courses/<int:sub_course_id>/edit/', views.edit_sub_course, name='edit_sub_course'),
    path('lessons/add/', views.add_lesson, name='add_lesson'),
    path('lessons/<int:lesson_id>/edit/', views.edit_lesson, name='edit_lesson'),
    path('logout/', views.CustomLogoutView.as_view(), name='custom_logout'),
    path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('send-password-reset/<int:user_id>/', views.send_password_reset, name='send_password_reset'),
    path('user-management/edit/<int:user_id>/', views.edit_user, name='customadmin_edit_user'),
    path('delete-user/<int:item_id>/', views.delete_user, name='delete_user'),
    path('user-management/', views.user_management, name='user_management'),
    path('view-user-quiz-details/<int:user_id>/', views.view_user_quiz_details, name='customadmin_view_user_quiz_details'),
    path('delete-multiple-users/', views.delete_multiple_users, name='delete_multiple_users'),
]
