from django.contrib import admin
from django.urls import path

from buisness_app import views

urlpatterns = [
    path('buisness/', views.index),
]