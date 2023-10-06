from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render


def index(request):
    return render(request, 'company.html')

# urlpatterns = [
#     # 공지사항
#     path('normal_notice/', (NormalNoticeView.as_view()), name='index'),
# ]