# eml_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_details, name='user_details'),
    path('upload_eml/<int:user_id>/', views.upload_eml, name='upload_eml'),
    path('feedback/<int:user_id>/', views.submit_feedback, name='submit_feedback'),
    path('thank_you/', views.thank_you, name='thank_you'),
]
