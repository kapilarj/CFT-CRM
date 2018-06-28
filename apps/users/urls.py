from django.urls import path, re_path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import (
    password_reset_done, password_reset, password_reset_confirm, password_reset_complete,
)


app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.auth_login, name='login'),
    path('register/', views.register, name='register'),
    path('login/profile/<int:id>/', views.profile, name='profile'),
    path('login/welcome/', views.welcome, name='welcome'),
    path('logout/', views.lout, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('sendemail/', views.sendEmail, name='sendmail'),
    path('token/', views.reset_password, name='token'),
    path('reset-link/<str:key>/', views.verify, name='verify'),
    path('reset-password/<str:token>/', views.reset_password, name='reset_password'),

    path('tmp/', TemplateView.as_view(template_name="apps/users/templates/users/tmp.html")),
    path('about/', TemplateView.as_view(template_name="static/production/index.html")),

]

