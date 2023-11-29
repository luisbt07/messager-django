from typing import Tuple
from django.contrib.sessions.models import Session
from django.utils import timezone

from django.db import transaction
import logging
logger = logging.getLogger(__name__)


from messaging.models import Message, MessageRecipient, CustomUser, MessageRequest


@transaction.atomic
def create_message_with_recipient(
        message_request: MessageRequest,
) -> Tuple[Message, MessageRecipient]:
    """
    :param message_request: Containing necessary parameters for the message creation
    :return: Message | Message Recipient
    """
    recipient_user = CustomUser.objects.filter(
        usercode=message_request.recipient_usercode
    ).last()
    if message_request.broadcast:
        raise AttributeError("Message with recipient can't be created with Broadcast argument")
    # only authenticated(created User) can reach here
    sender = CustomUser.objects.get(id=message_request.sender_id)
    if recipient_user:
        message = Message.objects.create(
            sender=sender,
            message=message_request.message,
            broadcast=False
        )
        recipient_message = MessageRecipient.objects.create(
            message=message,
            recipient=recipient_user
        )
    else:
        logger.info(
            msg="Recipient usercode: {} doesn't exists".format(message_request.recipient_usercode)
        )
        raise AttributeError(
            "There is no recipient with this code: {}".format(message_request.recipient_usercode)
        )
    return message, recipient_message

@transaction.atomic
def create_broadcast_message(message_request: MessageRequest) -> Message:
    sender = CustomUser.objects.get(id=message_request.sender_id)
    authenticated_users = fetch_all_online_users(current_user_id=sender.id)
    logger.info(authenticated_users)

    broadcast_message = Message.objects.create(
        sender=sender, message=message_request.message, broadcast=True
    )
    logger.info(broadcast_message)
    for recipient_user in authenticated_users:
        MessageRecipient.objects.create(
            message=broadcast_message,
            recipient=recipient_user
        )

    return broadcast_message


def fetch_all_online_users(current_user_id: int):
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = [int(session.get_decoded().get('_auth_user_id')) for session in active_sessions]
    # Exclude current_user_id
    logger.info(msg="current_user_id: {} user_ids: {}".format(current_user_id, user_ids))
    user_ids.remove(current_user_id)
    authenticated_users = CustomUser.objects.filter(
        id__in=user_ids
    )
    return authenticated_users