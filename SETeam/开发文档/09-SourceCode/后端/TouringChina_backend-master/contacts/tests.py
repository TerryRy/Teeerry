import unittest
from unittest.mock import patch
from django.test import RequestFactory
from views import ContactView, ContactIdView
from django.contrib.auth.models import User
from contacts.models import Contact
from datetime import datetime
from contacts.serializers import ContactSerializer
# Create your tests here.

class ContactViewTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = ContactView()

    def test_get_contacts(self):
        # 创建GET请求对象
        request = self.factory.get('/contacts/')
        # 设置用户对象
        user = User.objects.create(username='testuser', role='Common User')
        # 创建联系人对象
        contact1 = Contact.objects.create(name='John Doe', gender='M', birthdate='1990-01-01', id_card='1234567890', user=user)
        contact2 = Contact.objects.create(name='Jane Doe', gender='F', birthdate='1992-05-10', id_card='0987654321', user=user)
        # 调用视图方法进行测试
        response = self.view.get(request, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'contacts': ContactSerializer([contact1, contact2], many=True).data})

    def test_post_with_valid_data(self):
        # 创建POST请求对象
        request = self.factory.post('/contacts/', {'name': 'John Doe', 'gender': 'M', 'birthdate': '1990-01-01', 'id_card': '1234567890'})
        # 设置用户对象
        user = User.objects.create(username='testuser', role='Common User')
        # 调用视图方法进行测试
        response = self.view.post(request, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 0, 'message': "添加联系人成功"})
        # 确保联系人已添加
        self.assertEqual(user.contacts.count(), 1)
        contact = user.contacts.first()
        self.assertEqual(contact.name, 'John Doe')
        self.assertEqual(contact.gender, 'M')
        self.assertEqual(contact.birthdate, datetime.date(1990, 1, 1))
        self.assertEqual(contact.id_card, '1234567890')

    def test_post_with_missing_data(self):
        # 创建POST请求对象
        request = self.factory.post('/contacts/', {'name': 'John Doe', 'gender': 'M'})
        # 设置用户对象
        user = User.objects.create(username='testuser', role='Common User')
        # 调用视图方法进行测试
        response = self.view.post(request, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 1, 'message': "必须包含姓名、生日和身份证号"})
        # 确保联系人未添加
        self.assertEqual(user.contacts.count(), 0)

class ContactIdViewTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = ContactIdView()

    def test_delete_existing_contact(self):
        # 设置用户对象
        user = User.objects.create(username='testuser', role='Common User')
        # 创建联系人对象
        contact = Contact.objects.create(name='John Doe', gender='M', birthdate='1990-01-01', id_card='1234567890', user=user)
        contact_id = contact.id
        # 创建DELETE请求对象
        request = self.factory.delete('/contacts/' + contact_id)
        # 调用视图方法进行测试
        response = self.view.delete(request, contact_id, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 0, 'message': "成功删除联系人"})
        # 确保联系人已被删除
        self.assertFalse(user.contacts.filter(id=contact_id).exists())

    def test_delete_nonexistent_contact(self):
        # 设置用户对象
        user = User.objects.create(username='testuser', role='Common User')
        contact_id = 123456  # 假设不存在的联系人ID
        # 创建DELETE请求对象
        request = self.factory.delete('/contacts/' + contact_id)
        # 调用视图方法进行测试
        response = self.view.delete(request, contact_id, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 1, 'message': "未找到联系人"})

    def test_delete_contact_with_restricted_error(self):
        # 设置用户对象
        user = User.objects.create(username='testuser', role='Common User')
        # 创建联系人对象
        contact = Contact.objects.create(name='John Doe', gender='M', birthdate='1990-01-01', id_card='1234567890', user=user)
        contact_id = contact.id
        # 创建DELETE请求对象
        request = self.factory.delete('/contacts/' + contact_id)

        # 使用patch装饰器模拟RestrictedError
        with patch('views.Contact.delete') as mock_delete:
            mock_delete.side_effect = RestrictedError

            # 调用视图方法进行测试
            response = self.view.delete(request, contact_id, user)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'result': 1, 'message': "该联系人已经被用于购买车票，无法删除"})
            # 确保联系人未被删除
            self.assertTrue(user.contacts.filter(id=contact_id).exists())

class RestrictedError(Exception):
    pass

if __name__ == '__main__':
    unittest.main()
