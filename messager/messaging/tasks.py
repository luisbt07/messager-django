import logging
import time
from .celery import app
from .models import CustomUser, MessageRequest
from .services.message_service import create_message_with_recipient, create_broadcast_message

logger = logging.getLogger(__name__)


@app.task()
def web_task() -> None:
    logging.info("Starting web task...")
    time.sleep(10)
    logging.info("Done web task.")

@app.task()
def create_and_send_message(message_request: dict) -> dict:
    logging.info(
        msg="create_and_send_message_received: MessageRequest: {}".format(message_request)
    )
    # Deserialize message_request -> Transforma again into an MessageRequest instance
    message_request = MessageRequest.from_json_message_request(message_request)
    try:
        # When there is a recipient the message should be sent only to him/her
        if message_request.recipient_usercode:
            message, recipient_message = create_message_with_recipient(message_request)
            sender = message.sender
            return {
                'status': 'success',
                'message': message_request.message,
                'recipient_code': recipient_message.recipient.usercode,
                'sender_code': sender.usercode,
                'sender_name': sender.username,
                'broadcast': message_request.broadcast
            }
        # Broadcast message to all users authenticated
        else:
            broadcast_message = create_broadcast_message(message_request)
            sender = broadcast_message.sender

            return {
                'status': 'success',
                'message': message_request.message,
                'recipient_code': message_request.recipient_usercode,
                'sender_code': sender.usercode,
                'sender_name': sender.username,
                'broadcast': message_request.broadcast
            }
    except AttributeError as e:
        return {
            'status': 'error',
            'message': message_request.message,
            'sender_id': message_request.sender_id,
            'error_message': e.__str__()
        }
