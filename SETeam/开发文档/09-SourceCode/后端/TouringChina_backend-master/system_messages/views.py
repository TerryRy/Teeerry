from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView

from system_messages.models import Message
from system_messages.serializers import SentMessageSerializer, ReceivedMessageSerializer
from utils import json
from utils.perm import permission_check


# Create your views here.
class MessageView(APIView):
    @permission_check(user=True)
    def get(self, request, user):
        is_send = request.query_params.get('send', 'false').lower() == 'true'

        if is_send:
            return json.response({'system_messages': SentMessageSerializer(user.sent_messages.all(), many=True).data})
        else:
            return json.response({'system_messages': ReceivedMessageSerializer(user.received_messages.all(), many=True).data})

    @permission_check(['Train Admin', 'System Admin'], user=True)
    def post(self, request, user):
        message = request.data.get('message', "")
        to_users = request.data.get('to_users', None)

        if not to_users:
            return json.response({'result': 1, 'message': "消息必须设置接收人"})

        msg_to_send = Message(message=message, from_user=user)

        msg_to_send.save()

        for to_user_id in set(to_users):
            to_user = User.objects.filter(id=to_user_id).first()
            if to_user:
                msg_to_send.to_users.add(to_user)

        return json.response({'result': 0, 'message': "发送消息成功"})


class MessageIdView(APIView):
    @permission_check(user=True)
    def delete(self, request, message_id, user):
        message = user.sent_messages.filter(id=message_id).first()

        if not message:
            return json.response({'result': 1, 'message': "未找到要删除的消息"})

        message.delete()

        return json.response({'result': 0, 'message': "消息已删除"})
