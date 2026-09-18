"""Defines URL patterns for users """

from django.urls import path
from django.contrib.auth.views import LoginView
# from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # 登入頁面 (使用 Django 內建 View)
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),

    path('logout/', views.logout_view, name = 'logout'),

    path('register/', views.register_view, name='register'),

]
