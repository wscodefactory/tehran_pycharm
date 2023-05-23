from django.contrib import admin
from django.urls import path

from customer_app import views

urlpatterns = [
    path('customer/', views.index),
]