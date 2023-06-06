from django.test import TestCase

import json
from django.test import TestCase
from django.urls import reverse
from models import Message, User
# Create your tests here.

class MessageViewTestCase(TestCase):
    def setUp(self):
        # 创建测试用户
        self.user = User.objects.create(username='admin', password='admin123')

    def test_get_sent_messages(self):
        # 创建测试消息
        message = Message.objects.create(message='Test Message', from_user=self.user)
        message.to_users.add(self.user)

        # 使用API获取发送的系统消息
        url = reverse('/messages') + '?send=true'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # 验证响应的状态码
        self.assertEqual(response.status_code, 200)

        # 验证响应数据
        expected_data = {'system_messages': [{'id': message.id, 'message': 'Test Message'}]}
        self.assertJSONEqual(response.content, json.dumps(expected_data))

    def test_get_sent_messages(self):
        # 创建测试消息
        message = Message.objects.create(message='Test Message', from_user=self.user)
        message.to_users.add(self.user)

        # 使用API获取发送的系统消息
        url = reverse('/messages') + '?send=false'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)

        # 验证响应的状态码
        self.assertEqual(response.status_code, 200)

        # 验证响应数据
        expected_data = {'system_messages': [{'id': message.id, 'message': 'Test Message'}]}
        self.assertJSONEqual(response.content, json.dumps(expected_data))
