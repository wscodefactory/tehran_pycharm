from django.contrib import admin
from django.urls import path

from index import views

urlpatterns = [
    path('', views.index),
    path('login/', views.signin),
    path('login_page/', views.login_page),
    path('regist/', views.regist),
    path('register/', views.register),
    path('check_duplicate_id/', views.check_duplicate_id, name='check_duplicate_id'),
    path('logout/', views.logout_user, name='logout'),
]