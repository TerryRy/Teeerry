from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Message(models.Model):
    message = models.TextField(max_length=500)
    send_time = models.DateTimeField(auto_now_add=True)

    from_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    to_users = models.ManyToManyField(to=User, related_name='received_messages')
