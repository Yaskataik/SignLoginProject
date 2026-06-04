from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # --- ADD THIS BLOCK ---
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already taken.'}, status=400)
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # ----------------------
            
            return JsonResponse({'message': 'Registration successful!'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'error': 'No user found with this email.'}, status=401)
            
            # This is the exact moment of truth
            user = authenticate(username=user_obj.username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'message': 'Login successful!'}, status=200)
            else:
                # If we get here, the user was found but the password was wrong
                return JsonResponse({'error': 'Password does not match.'}, status=401)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)