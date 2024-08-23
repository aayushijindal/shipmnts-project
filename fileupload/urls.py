from django.urls import path

from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('confirm/', views.confirm_upload, name='confirm_upload'),
]
