from django.urls import path
from .views import SignupView, LoginView, RequestPasswordReset, ConfirmPasswordReset

urlpatterns = [
    # Auth paths
    path('register/', SignupView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # Password Reset paths
    path('request-reset/', RequestPasswordReset.as_view(), name='request-reset'),
    path('password-reset-confirm/<str:uidb64>/<str:token>/', ConfirmPasswordReset.as_view(), name='password-reset-confirm'),
]