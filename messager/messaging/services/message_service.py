from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Tuple, List
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.db import transaction
from itertools import chain

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


def fetch_historical_by_count_messages(user_id:int, count_messages=10) -> List[dict]:
    # By default, the fetch_historical will consider the last 10 messages(sent or received)

    # Avoiding timeout when having lots of messages
    date_filter = datetime.now() - relativedelta(month=1)
    user = CustomUser.objects.get(id=user_id)
    sent_messages = user.sent_messages.filter(created_at__gt=date_filter)
    received_messages = user.received_messages.filter(created_at__gt=date_filter)
    logger.info("user: {} - message_sent: {} - received_messages: {} - date_filter: {}".format(
        user, sent_messages, received_messages, date_filter)
    )
    # Combine sent and received messages into a single queryset retrieve last 10
    last_messages = sorted(
        chain(sent_messages, received_messages),
        key=lambda x: x.created_at, reverse=False
    )[:count_messages]

    historical_messages = build_historical_messages_json(last_messages)
    return historical_messages


def build_historical_messages_json(all_messages):
    historical_messages = []
    for message_instance in all_messages:
        if isinstance(message_instance, Message):
            historical_messages.append({
                'sender_name': message_instance.sender.username,
                'sender_code': message_instance.sender.usercode,
                'message': message_instance.message,
                'created_at': message_instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        else: # isntance of MessageRecipient
            historical_messages.append({
                'sender_name': message_instance.message.sender.username,
                'sender_code': message_instance.message.sender.usercode,
                'message': message_instance.message.message,
                'created_at': message_instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
    return historical_messages
