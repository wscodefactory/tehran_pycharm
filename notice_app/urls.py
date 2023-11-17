from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from notice_app import views

urlpatterns = [
    path('notice/', views.notice_list, name='notice_list'),
    path('create_notice_page/', views.create_notice_page),
    path('create_notice/', views.create_notice),
    path('notice_detail/<int:id>/', views.notice_detail, name='notice_detail'),
    path('notice_update/<int:id>/', views.notice_update, name='notice_update'),
    path('notice_delete/<int:id>/', views.notice_delete, name='notice_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
