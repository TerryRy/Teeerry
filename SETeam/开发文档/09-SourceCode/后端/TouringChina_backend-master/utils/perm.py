from datetime import datetime

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from jwt import DecodeError

from utils import json


class permission_check:
    def __init__(self, roles: list = None, user: bool = False):
        self.roles = roles
        self.set_user = user

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            request = args[-1]
            req_jwt = request.headers.get('jwt', "")

            try:
                info = jwt.decode(req_jwt, settings.SECRET_KEY, "HS256")
            except DecodeError as e:
                return json.response({'result': 1, 'message': "无法解析 JWT"})

            expire = datetime.fromisoformat(info['expire'])

            if expire < datetime.now():
                return json.response({'result': 1, 'message': "登陆已过期，请重新登录"})

            id = info['id']
            if not User.objects.filter(id=id).exists():
                return json.response({'result': 1, 'message': "找不到用户"})
            user = User.objects.get(id=id)

            if not (self.roles is None or user.groups.filter(name__in=self.roles).exists()):
                return json.response({'result': 1, 'message': "无权访问"})

            if self.set_user:
                kwargs['user'] = user

            return func(*args, **kwargs)

        return wrapper
