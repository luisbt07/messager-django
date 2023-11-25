from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import logging
import json

from messaging.tasks import verify_and_send_message

logger = logging.getLogger(__name__)


def messaging(request):
    return render(request, 'messaging_app/index.html', {})

# ignore authentication
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Celery async execution task
            task_result = verify_and_send_message.delay(data)
            logger.info("Message is being processed by celery")
            # waits the result of the task to continue
            result = task_result.get()
            return JsonResponse(
                result
            )
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error'}, status=400)
    return JsonResponse({'status': 'error'}, status=405)
