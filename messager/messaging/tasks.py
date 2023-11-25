import json
from django.http import JsonResponse
import logging
import time
from .celery import app


@app.task()
def web_task() -> None:
    logging.info("Starting web task...")
    time.sleep(10)
    logging.info("Done web task.")

@app.task()
def verify_and_send_message(data: dict):
    message = data.get('message')
    recipient = data.get('recipient')
    logging.info(message, recipient)
    # Perform actions with the message and recipient as needed
    # You might save the message to a database, process it, or send it to other users

    # Create a dictionary representing the JSON response data
    response_data = {
        'status': 'success',
        'message': message,
        'recipient': recipient
    }
    return response_data
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:luisbt07/messager-django.git
git push -u origin main