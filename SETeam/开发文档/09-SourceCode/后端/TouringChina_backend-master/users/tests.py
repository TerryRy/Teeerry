from audioop import reverse
import datetime
import mailbox
from django.conf import settings
from django.test import TestCase
from datetime import timedelta
from django.contrib.auth.models import User
import jwt
from rest_framework.test import APIClient, APIRequestFactory

from users.views import UserIdView, UserView, get_current_user
# Create your tests here.
class StartRegisterTestCase(TestCase):
    def test_start_register(self):
        # 准备测试数据
        name = 'testuser'
        passwd = 'testpassword'
        email = 'test@example.com'
        host = 'localhost'
        
        # 模拟请求数据
        request_data = {
            'name': name,
            'passwd': passwd,
            'email': email,
            'host': host
        }

        # 发送请求
        url = reverse('/users/register')  # 假设URL名称为'start-register'
        response = self.client.post(url, data=request_data)

        # 验证响应的状态码
        self.assertEqual(response.status_code, 200)

        # 验证用户是否被成功创建
        self.assertTrue(User.objects.filter(username=name).exists())

        # 验证邮件发送是否成功
        self.assertEqual(len(mailbox.outbox), 1)
        self.assertEqual(mailbox.outbox[0].subject, '畅游中国用户注册')
        self.assertEqual(mailbox.outbox[0].to, [email])

        # 验证响应数据
        expected_data = {'result': 0, 'message': "已发送认证邮件"}
        self.assertJSONEqual(response.content, expected_data)

        # 验证已存在用户无法再次注册
        user_exists_response = self.client.post(url, data=request_data)
        expected_error_data = {'result': 1, 'message': "用户名已被注册"}
        self.assertJSONEqual(user_exists_response.content, expected_error_data)

    def test_verify_register(self):
        # 准备测试数据
        name = 'testuser'
        passwd = 'testpassword'
        email = 'test@example.com'
        expire = (datetime.now() + datetime.timedelta(hours=2)).isoformat()
        code = jwt.encode(
            {
                'name': name,
                'passwd': passwd,
                'email': email,
                'expire': expire
            },
            settings.SECRET_KEY,
        )

        # 构造URL
        url = f"/users/register/{code}"
        # 发送GET请求
        response = self.client.get(url)

        # 验证响应的状态码
        self.assertEqual(response.status_code, 200)

        # 验证用户是否被成功创建
        self.assertTrue(User.objects.filter(username=name, email=email).exists())

        # 验证已注册的邮箱无法再次注册
        existing_email_response = self.client.get(url)
        self.assertEqual(existing_email_response.status_code, 200)
        self.assertContains(existing_email_response, "用户已被注册")

        # 验证已过期的认证码无法注册
        expired_code = jwt.encode(
            {
                'name': 'expireduser',
                'passwd': 'expiredpassword',
                'email': 'expired@example.com',
                'expire': (datetime.now() - timedelta(hours=2)).isoformat()
            },
            settings.SECRET_KEY,
        )
        expired_code_url = reverse(f"/users/register/{code}", args=[expired_code])
        expired_response = self.client.get(expired_code_url)
        self.assertEqual(expired_response.status_code, 200)
        self.assertContains(expired_response, "认证已过期")

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_login_with_valid_credentials(self):
        # 创建一个用户对象
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        # 构建登录请求数据
        data = {
            'name': 'testuser',
            'email': 'test@example.com',
            'passwd': 'testpassword'
        }

        # 发送登录请求
        response = self.client.post(reverse('/users/login'), data, format='json')

        # 断言响应状态码和返回结果
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['result'], 0)
        self.assertEqual(response.data['message'], "登陆成功")

        # 验证JWT令牌
        decoded_token = jwt.decode(response.data['jwt'], settings.SECRET_KEY, algorithms=['HS256'])
        self.assertEqual(decoded_token['id'], user.id)

        # 验证令牌过期时间
        expire = datetime.fromisoformat(decoded_token['expire'])
        expected_expire = datetime.now() + timedelta(hours=2)
        self.assertAlmostEqual(expire, expected_expire, delta=timedelta(seconds=5))

    def test_login_with_invalid_credentials(self):
        # 创建一个用户对象
        User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

        # 构建登录请求数据（密码错误）
        data = {
            'name': 'testuser',
            'email': 'test@example.com',
            'passwd': 'incorrectpassword'
        }

        # 发送登录请求
        response = self.client.post(reverse('/users/login'), data, format='json')

        # 断言响应状态码和返回结果
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "密码不正确")

    def test_login_with_invalid_user(self):
        # 构建登录请求数据（用户不存在）
        data = {
            'name': 'nonexistentuser',
            'email': 'nonexistent@example.com',
            'passwd': 'testpassword'
        }

        # 发送登录请求
        response = self.client.post(reverse('/users/login'), data, format='json')

        # 断言响应状态码和返回结果
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "未找到用户，请检查邮箱或用户名是否正确")

class UserViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_users(self):
        # Create some test users
        user1 = User.objects.create(username='user1', email='user1@example.com')
        user2 = User.objects.create(username='user2', email='user2@example.com')

        # Create a GET request
        request = self.factory.get('/users/')

        # Instantiate the UserView and call the get method
        view = UserView.as_view()
        response = view(request)

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['users']), 2)

        # Clean up the test users
        user1.delete()
        user2.delete()

    def test_add_user(self):
        # Create a POST request with user data
        data = {
            'name': 'newuser',
            'passwd': 'password',
            'email': 'newuser@example.com',
            'role': ['Common User', 'Train Admin'],
        }
        request = self.factory.post('/users/', data)

        # Instantiate the UserView and call the post method
        view = UserView.as_view()
        response = view(request)

        # Assert the response status code and data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['result'], 0)
        self.assertEqual(response.data['message'], "添加用户成功")

        # Check if the user was created and assigned to the correct groups
        user = User.objects.get(username='newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.groups.count(), 2)
        self.assertTrue(user.groups.filter(name='Common User').exists())
        self.assertTrue(user.groups.filter(name='Train Admin').exists())

        # Clean up the test user
        user.delete()

class UserIdViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = UserIdView.as_view()
        self.user = User.objects.create(username='testuser', email='test@example.com')

    def test_put_user_exists(self):
        request_data = {
            'name': 'updated_user',
            'passwd': 'updated_password',
            'email': 'updated_email@example.com',
            'role': ['Role1', 'Role2'],
        }
        request = self.factory.put('/users/10', data=request_data)
        response = self.view(request, user_id=10)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['result'], 0)
        self.assertEqual(response.data['message'], "更新用户数据成功")

        # Assert user fields are updated
        updated_user = User.objects.get(id=10)
        self.assertEqual(updated_user.username, 'updated_user')
        self.assertEqual(updated_user.check_password('updated_password'), True)
        self.assertEqual(updated_user.email, 'updated_email@example.com')
        self.assertEqual(updated_user.groups.count(), 2)

    def test_put_user_not_found(self):
        request_data = {
            'name': 'updated_user',
            'passwd': 'updated_password',
            'email': 'updated_email@example.com',
            'role': ['Role1', 'Role2'],
        }
        request = self.factory.put('/users/999', data=request_data)
        response = self.view(request, user_id=999)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "用户不存在")

    def test_delete_user_exists(self):
        request = self.factory.delete('/users/10')
        response = self.view(request, user_id=10)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['result'], 0)
        self.assertEqual(response.data['message'], "用户已删除")

        # Assert user is deleted
        with self.assertRaises(User.DoesNotExist):
            deleted_user = User.objects.get(id=10)

    def test_delete_user_not_found(self):
        request = self.factory.delete('/users/999')
        response = self.view(request, user_id=999)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['result'], 1)
        self.assertEqual(response.data['message'], "用户不存在")

class GetCurrentUserTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = get_current_user

    def test_get_current_user(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        request = self.factory.get('/users/me')
        request.user = user
        response = self.view(request, user=user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'username': 'testuser', 'email': 'test@example.com'})

    def test_get_current_user_unauthenticated(self):
        request = self.factory.get('/users/me')
        response = self.view(request, user=None)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {'detail': 'Authentication credentials were not provided.'})
