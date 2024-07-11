# /Users/Julia/Downloads/braine-package/myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blog-classic/', views.blogclassic, name='blogclassic'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('index-2/', views.index2, name='index2'),
    path('index-3/', views.index3, name='index3'),
    path('login/', views.login, name='login'),
    path('news-detail/', views.newsdetail, name='newsdetail'),
    path('not-found/', views.notfound, name='notfound'),
    path('pricing/', views.pricing, name='pricing'),
    path('register/', views.register, name='register'),
    path('reset/', views.reset, name='reset'),
    path('service-detail/', views.servicedetail, name='servicedetail'),
    path('services/', views.services, name='services'),
    path('team-detail/', views.teamdetail, name='teamdetail'),
    path('team/', views.team, name='team'),
    path('testimonial/', views.testimonial, name='testimonial'),
]
