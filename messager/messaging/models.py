import json
import random
import string
from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint


class CustomUser(User):
    usercode = models.CharField(max_length=6, unique=True, db_index=True)
    def save(self, *args, **kwargs):
        if not self.pk or not self.usercode:
            unique_code = self._generate_unique_usercode()
            self.usercode = unique_code

        super().save(*args, **kwargs)
    def _generate_unique_usercode(self):
        while True:
            new_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not CustomUser.objects.filter(usercode=new_code).exists():
                return new_code
    class Meta:
        constraints = [
            UniqueConstraint(fields=['usercode'], name='unique_usercode')
        ]


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.CharField(max_length=255)
    broadcast = models.BooleanField(default=False) # If message was sent to all online users

class MessageRecipient(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='recipients')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')


class MessageRequest:
    def __init__(self, sender_id, message, recipient_usercode=None):
        self.sender_id = sender_id
        self.message = message
        self.recipient_usercode = recipient_usercode
        self.broadcast = bool(not recipient_usercode) # broadcast if recipient not provided

    @classmethod
    def from_request(cls, request):
        data = json.loads(request.body)
        sender_id = request.user.id
        message = data.get('message', None)
        recipient_usercode = data.get('recipient', None)
        return cls(sender_id, message, recipient_usercode)

    @classmethod
    def from_json_message_request(cls, json_message_request):
        return MessageRequest(
            sender_id=json_message_request.get('sender_id'),
            message=json_message_request.get('message'),
            recipient_usercode=json_message_request.get('recipient_usercode'),
        )

    def __json__(self):
        return {
            'sender_id': self.sender_id,
            'message': self.message,
            'recipient_usercode': self.recipient_usercode,
            'broadcast': self.broadcast,
        }
