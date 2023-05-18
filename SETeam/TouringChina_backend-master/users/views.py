from datetime import datetime, timedelta
from smtplib import SMTPException

import jwt
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template.loader import render_to_string
from jwt import DecodeError
from rest_framework.decorators import api_view
from rest_framework.views import APIView

import utils.mail
from users.serializers import UserSerializer
from utils import json
from utils.perm import permission_check


# Create your views here.
@api_view(['POST'])
def start_register(request):
    name = request.data.get('name', "")
    passwd = request.data.get('passwd', "")
    email = request.data.get('email', "")

    if User.objects.filter(username=name).exists():
        return json.response({'result': 1, 'message': "用户名已被注册"})

    if User.objects.filter(email=email).exists():
        return json.response({'result': 1, 'message': "邮箱已被注册"})

    code = jwt.encode(
        {
            'name': name,
            'passwd': passwd,
            'email': email,
            'expire': (datetime.now() + timedelta(hours=2)).isoformat()
        },
        settings.SECRET_KEY,
    )

    try:
        utils.mail.send_mail(
            "畅游中国用户注册",
            "请按提示完成注册验证",
            render_to_string("verify_link.html", {'url': f"{request.build_absolute_uri()}/{code}"}),
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
        )
    except SMTPException as e:
        return json.response({'result': 1, 'message': f"邮件发送失败，{e}"})

    return json.response({'result': 0, 'message': "已发送认证邮件"})


@api_view(['GET'])
def verify_register(request, code):
    try:
        info = jwt.decode(code, settings.SECRET_KEY, "HS256")
    except DecodeError:
        return json.response({'result': 1, 'message': "无法解析 JWT"})

    name = info['name']
    passwd = info['passwd']
    email = info['email']
    expire = datetime.fromisoformat(info['expire'])

    if expire < datetime.now():
        HttpResponse("认证已过期")

    if User.objects.filter(email=email).exists():
        return HttpResponse("用户已被注册")

    user = User.objects.create_user(name, email, passwd)
    common_group, _ = Group.objects.get_or_create(name="Common User")
    user.groups.add(common_group)

    return HttpResponse("注册成功！")


@api_view(['POST'])
def login(request):
    name = request.data.get('name', None)
    email = request.data.get('email', None)
    passwd = request.data.get('passwd', "")

    if name and User.objects.filter(username=name).exists():
        user = User.objects.get(username=name)
    elif email and User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
    else:
        return json.response({'result': 1, 'message': "未找到用户，请检查邮箱或用户名是否正确"})

    if not user.check_password(passwd):
        return json.response({'result': 1, 'message': "密码不正确"})

    user_jwt = jwt.encode(
        {
            'id': user.id,
            'expire': (datetime.now() + timedelta(hours=2)).isoformat(),
        },
        settings.SECRET_KEY,
    )

    return json.response({'result': 1, 'message': "登陆成功", 'jwt': user_jwt})


class UserView(APIView):
    @permission_check(['System Admin'])
    def get(self, request):
        """
        list all users, permission "System Admin" is required
        """
        return json.response({'users': [UserSerializer(u).data for u in User.objects.all()]})

    @permission_check(['System Admin'])
    def post(self, request):
        """
        add new user, permission "System Admin" is required
        """
        name = request.data.get('name', None)
        passwd = request.data.get('passwd', "")
        email = request.data.get('email', None)
        roles = request.data.get('role', None)

        if name is None:
            return json.response({'result': 1, 'message': "必须包含用户名"})

        if User.objects.filter(username=name).exists():
            return json.response({'result': 1, 'message': "用户名已存在"})

        if email and User.objects.filter(email=email).exists():
            return json.response({'result': 1, 'message': "邮箱已存在"})

        user = User.objects.create_user(name, email, passwd)

        if roles:
            for role in roles:
                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)

        return json.response({'result': 0, 'message': "添加用户成功"})


class UserIdView(APIView):
    @permission_check(['System Admin'])
    def put(self, request, user_id):
        if not User.objects.filter(id=user_id).exists():
            json.response({'result': 1, 'message': "用户不存在"})

        user = User.objects.get(id=user_id)

        name = request.data.get('name', None)
        passwd = request.data.get('passwd', None)
        email = request.data.get('email', None)
        roles = request.data.get('role', None)

        if name and not User.objects.filter(username=name).exists():
            user.username = name

        if passwd:
            user.password = passwd

        if email:
            user.email = email

        if roles:
            user.groups.clear()
            for role in roles:
                group, _ = Group.objects.get_or_create(name=role)
                user.groups.add(group)

        try:
            user.save()
        except ValidationError as e:
            return json.response({'result': 1, 'message': f"更新用户数据失败，{e}"})

        return json.response({'result': 0, 'message': "更新用户数据成功"})

    @permission_check(['System Admin'])
    def delete(self, request, user_id):
        if not User.objects.filter(id=user_id).exists():
            return json.response({'result': 1, 'message': "用户不存在"})

        user = User.objects.get(id=user_id)

        user.delete()

        return json.response({'result': 0, 'message': "用户已删除"})
