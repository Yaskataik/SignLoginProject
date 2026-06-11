from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import SimpleRateThrottle
from rest_framework.views import APIView

from .serializers import UserSerializer

class EmailTargetRateThrottle(SimpleRateThrottle):
    """
    Throttles based on the targeted email address rather than the client IP.
    This prevents attackers from bypassing limits by rotating IP addresses via VPNs/Proxies.
    """
    scope = 'login_email'

    def get_cache_key(self, request, view):
        # We only apply this to POST login requests providing an email
        if request.method != 'POST':
            return None
            
        email = request.data.get('email')
        if not email:
            return None

        # Fix: Use the raw string directly instead of running self.get_ident()
        return self.cache_format % {
            'scope': self.scope,
            'ident': email.strip().lower()
        }



# 1. Signup View
class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2. Login View
class LoginView(APIView):
    # Apply our custom email target throttle class here
    throttle_classes = [EmailTargetRateThrottle] 

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



# 1. Request Password Reset (The Token Generator)
class RequestPasswordReset(APIView):
    permission_classes = [] 

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        
        # Security: Always return 200 OK, even if the user isn't found.
        # This prevents 'Email Enumeration' side-channel attacks.
        if user and user.is_active:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            reset_link = f"http://localhost:5173/reset-password-confirm/{uid}/{token}"
            
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
        return Response({"message": "If that email exists, a reset link has been sent."}, status=status.HTTP_200_OK)


# 2. Confirm Password Reset (The Validator)
class ConfirmPasswordReset(APIView):
    permission_classes = []

    def post(self, request, uidb64, token):
        try:
            # Decode the user ID from the URL
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"message": "Invalid link."}, status=status.HTTP_400_BAD_REQUEST)

        # Verify the security token
        if default_token_generator.check_token(user, token):
            new_password = request.data.get('password')
            if new_password:
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successfully!"}, status=status.HTTP_200_OK)
            return Response({"message": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)