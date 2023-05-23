from django.contrib import admin
from django.urls import path

from product_app import views

urlpatterns = [
    path('product/', views.index),
]