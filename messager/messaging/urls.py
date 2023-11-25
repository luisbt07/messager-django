from django.urls import path
from messaging import views

urlpatterns = [
    path('', views.messaging, name='messaging'),
    path('send_message/', views.send_message, name='send_message'),
]