from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# 1. Signup View
class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle # 1. Import this
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# 2. Login View
class LoginView(APIView):
    throttle_classes = [AnonRateThrottle] 

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
            if user:
                login(request, user)
                return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
            return Response({'error': 'Password does not match.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'No user found with this email.'}, status=status.HTTP_401_UNAUTHORIZED)

from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# 1. SENDING THE EMAIL (The Token Generator)
class RequestPasswordReset(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # This is the link the user clicks in their email
            reset_url = f"http://localhost:5173/reset-password-confirm/{uid}/{token}/"
            
            send_mail(
                'Password Reset Request',
                f'Use this link to reset your password: {reset_url}',
                'noreply@yourcompany.com',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Reset link sent to your email.'})
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

# 2. UPDATING THE PASSWORD (The Validator)
class ConfirmPasswordReset(APIView):
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        
        token_generator = PasswordResetTokenGenerator()
        if token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful!'})
        return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

class RequestPasswordReset(APIView):
    # Allow anyone to request a reset, no login needed
    permission_classes = [] 

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        
        # Security: Always return 200 OK, even if the user isn't found
        # This prevents 'Email Enumeration' attacks.
        if user and user.is_active:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Use your production URL here when you deploy!
            reset_link = f"http://localhost:5173/reset-password-confirm/{uid}/{token}"
            
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
        return Response({"message": "If that email exists, a reset link has been sent."}, status=status.HTTP_200_OK)

        from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

class ConfirmPasswordReset(APIView):
    permission_classes = []

    def post(self, request, uidb64, token):
        try:
            # Decode the user ID from the URL
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"message": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the token
        if default_token_generator.check_token(user, token):
            new_password = request.data.get('password')
            if new_password:
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successfully!"}, status=status.HTTP_200_OK)
            return Response({"message": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)