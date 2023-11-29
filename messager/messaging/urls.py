from django.urls import path
from messaging import views

urlpatterns = [
    path('', views.messager, name='messager'),
    path('send_message/', views.send_message, name='send_message'),
    path('enter_message_app/register_user/', views.register_user, name='register_user'),
    path('enter_message_app/login_user/', views.login_user, name='login_user'),
    path('enter_message_app/', views.enter_message_app, name='enter_message_app'),
    path('fetch_online_users/', views.fetch_online_users, name='fetch_online_users'),
]