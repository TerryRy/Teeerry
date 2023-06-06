from django.contrib.auth.models import User
from accounts.models import Account
import unittest
from django.test import RequestFactory
from accounts.serializers import AccountSerializer
from views import AccountView, AccountIdView

# Create your tests here.

class AccountViewTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = AccountView()

    def test_post_with_missing_fields(self):
        request = self.factory.post('/accounts/', {'account_name': 'Test Account'})
        user = User.objects.create(username='user', role='Common User')
        response = self.view.post(request, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 1, 'message': "必须填写持卡人和卡号"})

    def test_post_with_existing_card(self):
        # Assuming user is a pre-existing user with some accounts
        request = self.factory.post('/accounts/', {
            'account_name': 'Test Account',
            'card_holder_name': 'John Doe',
            'card_id': '1234567890'
        })
        user = User.objects.create(username='user', role='Common User')
        response = self.view.post(request, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 1, 'message': "该银行卡已经被添加过了"})

    def test_post_with_successful_verification(self):
        # Assuming verify_account(card_id, card_holder_name) returns True
        request = self.factory.post('/accounts/', {
            'account_name': 'Test Account',
            'card_holder_name': 'John Doe',
            'card_id': '1234567890'
        })
        user = User.objects.create(username='user', role='Common User')
        response = self.view.post(request, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 0, 'message': "创建账户成功"})

    def test_post_with_failed_verification(self):
        # Assuming verify_account(card_id, card_holder_name) returns False
        request = self.factory.post('/accounts/', {
            'account_name': 'Test Account',
            'card_holder_name': 'John Doe',
            'card_id': '1234567890'
        })
        user = User.objects.create(username='user', role='Common User')
        response = self.view.post(request, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 1, 'message': "银行卡信息认证未通过"})

    def test_post_with_wrong_role(self):
        request = self.factory.post('/accounts/', {
            'account_name': 'Test Account',
            'card_holder_name': 'John Doe',
            'card_id': '1234567890'
        })
        user = User.objects.create(username='user', role='Train Admin')
        response = self.view.post(request, user)
        self.assertEqual(response.status_code, 403) 

    def test_get_with_common_user_permission(self):
        # 创建GET请求对象
        request = self.factory.get('/accounts/')
        # 设置用户对象
        user = User.objects.create(username='testuser', role='Common User')
        # 调用视图方法进行测试
        response = self.view.get(request, user)
        self.assertEqual(response.status_code, 200)
        # 对返回的数据进行断言
        expected_data = {
            'accounts': [AccountSerializer(ac).data for ac in user.accounts.all()]
        }
        self.assertEqual(response.json(), expected_data)

    def test_get_with_admin_user_permission(self):
        # 创建GET请求对象
        request = self.factory.get('/accounts/')
        # 设置用户对象
        user = User.objects.create(username='adminuser', role='Admin')
        # 调用视图方法进行测试
        response = self.view.get(request, user)
        self.assertEqual(response.status_code, 403) 

class AccountIdViewTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = AccountIdView()

    def test_delete_existing_account(self):
        # 设置用户对象
        user = User.objects.create(username='testuser', role='Common User')
        # 创建DELETE请求对象
        request = self.factory.delete('/accounts/'+user.id)
        # 创建账户对象
        account = Account.objects.create(name='Test Account', card_id='1234567890', user=user)
        account_id = account.id
        # 调用视图方法进行测试
        response = self.view.delete(request, account_id, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 0, 'message': "成功删除账户"})
        # 确保账户已被删除
        self.assertFalse(user.accounts.filter(id=account_id).exists())

    def test_delete_nonexistent_account(self):
        # 设置用户对象
        user = User.objects.create(username='testuser', role='Common User')
        # 创建DELETE请求对象
        request = self.factory.delete('/accounts/'+user.id)
        account_id = 123456  # 假设不存在的账户ID
        # 调用视图方法进行测试
        response = self.view.delete(request, account_id, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 1, 'message': "该账户不存在"})

    def test_put_with_valid_data(self):
        # 设置用户对象
        user = User.objects.create(username='testuser', role='Common User')
        # 创建PUT请求对象
        request = self.factory.put('/accounts/'+user.id, {'amount': '100.00'})
        # 创建账户对象
        account = Account.objects.create(name='Test Account', card_id='1234567890', user=user)
        account_id = account.id
        # 调用视图方法进行测试
        response = self.view.put(request, account_id, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 0, 'message': "充值成功"})
        # 确保账户金额已更新
        account.refresh_from_db()
        self.assertEqual(account.amount, 100.00)

    def test_put_with_missing_amount(self):
        # 设置用户对象
        user = User.objects.create(username='testuser', role='Common User')
        # 创建PUT请求对象
        request = self.factory.put('/accounts/'+user.id)
        account_id = 123456  # 假设存在的账户ID
        # 调用视图方法进行测试
        response = self.view.put(request, account_id, user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'result': 1, 'message': "必须输入金额"})

if __name__ == '__main__':
    unittest.main()
