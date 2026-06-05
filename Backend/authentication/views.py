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

# 2. Login View
class LoginView(APIView):
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

# 3. Reset Password View
class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password successfully reset!'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User with this email not found.'}, status=status.HTTP_404_NOT_FOUND)