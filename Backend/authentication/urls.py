from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.signup_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('reset-password/', views.reset_password_view, name='reset_password'), # Add this line
]