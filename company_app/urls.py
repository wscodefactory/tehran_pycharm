from django.contrib import admin
from django.urls import path

from company_app import views

urlpatterns = [
    path('company/', views.index),
]