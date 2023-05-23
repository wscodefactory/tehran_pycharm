from django.contrib import admin
from django.urls import path

from notice_app import views

urlpatterns = [
    path('notice/', views.index),
]