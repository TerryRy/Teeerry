from django.test import TestCase
import unittest

from utils import json
from views import AccountView


# Create your tests here.

class Case(unittest.TestCase):
    def setUp(self):
        self.test_class = AccountView()

    def test_post_5_5(self):
        self.assertEqual(self.test_class.post(self, 123, 123), json.response({'result': 1, 'message': "必须填写持卡人和卡号"}))
    # def test_bool_value(self):
    #     self.assertTrue(self.test_class.is_string("hello world!"))
    # def test_raise(self):
    #     self.assertRaises(KeyError, self.test_class.raise_error)
    # def tearDown(self):
    #     del self.test_class


if __name__ == "__main__":
    unittest.main()
