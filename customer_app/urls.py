from django.contrib import admin
from django.urls import path

from customer_app import views

urlpatterns = [
    path('customer/', views.qna_list, name='qna_list'),
    path('search/', views.search_qna, name='search_qna'),
    path('create_qna_page/', views.create_qna_page),
    path('ask_question/', views.ask_question),
    path('qna_detail/<int:id>/', views.qna_detail, name='qna_detail'),
    path('answer_add/<int:id>/', views.answer_add, name='answer_add'),
    path('answer_update/<int:id>/', views.answer_update, name='answer_update'),
    path('answer_delete/<int:id>/', views.answer_delete, name='answer_delete'),
]