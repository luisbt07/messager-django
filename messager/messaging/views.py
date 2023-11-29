from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from messaging.models import CustomUser, MessageRequest
from messaging.services.message_service import fetch_all_online_users
import logging
import json

from .tasks import create_and_send_message

logger = logging.getLogger(__name__)

def enter_message_app(request):
    if request.method == 'GET':
        return render(request, 'messaging_app/login.html', {})

@csrf_exempt
def login_user(request):
    if request.user.is_authenticated:
        return redirect('messager')
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('messager')
        else:
            # Return an error message if authentication fails
            error_message = 'Invalid username or password. Please try again.'
            JsonResponse({'status': 'error', "message": error_message}, status=400)
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data['username']
            email = data['email']
            password = data['password']
            # Check if the username already exists
            if CustomUser.objects.filter(username=username).exists():
                error_message = 'Username is already taken. Please choose a different one.'
                return render(request, 'messaging_app/login.html', {'error_message': error_message})

            # Create a new user
            user = CustomUser.objects.create_user(username=username, email=email, password=password)
            # login(request, user)  # Automatically log in the user after registration
            # Redirect to a success page or home page after registration
            return JsonResponse({'status': 'Ok'}, status=200)  # Replace 'home' with your desired URL name
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def messager(request):
    return render(request, 'messaging_app/messager.html')


# Locally is not possible to generate cookies in an easy way.
@csrf_exempt
@login_required
def send_message(request):
    if request.method == 'POST':
        try:
            # Celery can't serialize automatically a class
            # it was necessary to convert to json(that is serializable)
            message_request = MessageRequest.from_request(request).__json__()

            # Celery async execution create and sengind tasks
            message_task_result = create_and_send_message.delay(message_request)
            logger.info("Message is being processed by celery defualt Queue")
            # waits the result of the task to continue
            result = message_task_result.get()
            return JsonResponse(result)
        except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'JsonDecodeError'}, status=400)
    return JsonResponse({'status': 'error'}, status=405)


@csrf_exempt
@login_required
def get_online_users(request):
    current_user_id = request.user.id
    # Getting active sessions using celery
    online_users = fetch_all_online_users(current_user_id=current_user_id)
    online_user_values = list(online_users.values("usercode","username"))
    # waits the result of the task to continue
    return JsonResponse({"online_users": online_user_values}, status=200)
