from rest_framework import serializers

from contacts.models import Contact
from system_messages.models import Message


class SentMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ['from_user']


class ReceivedMessageSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()

    class Meta:
        model = Message
        exclude = ['to_users']

    def get_from_user(self, obj):
        return obj.from_user.username
