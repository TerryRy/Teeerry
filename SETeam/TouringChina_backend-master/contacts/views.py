from datetime import datetime

from django.db.models import RestrictedError
from rest_framework.views import APIView

from contacts.models import Contact
from contacts.serializers import ContactSerializer
from utils import json
from utils.perm import permission_check


# Create your views here.
class ContactView(APIView):
    @permission_check(['Common User'], user=True)
    def get(self, request, user):
        return json.response({'contacts': ContactSerializer(user.contacts, many=True).data})

    @permission_check(['Common User'], user=True)
    def post(self, request, user):
        name = request.data.get('name', None)
        gender = request.data.get('gender', "U")
        birthdate = request.data.get('birthdate', None)
        id_card = request.data.get('id_card', None)

        if not name or not birthdate or not id_card:
            return json.response({'result': 1, 'message': "必须包含姓名、生日和身份证号"})

        birthdate = datetime.fromisoformat(birthdate)

        if gender not in ["M", "F", "U"]:
            return json.response({'result': 1, 'message': "性别必须为 M 或 F"})

        if user.contacts.filter(id_card=id_card).exists():
            return json.response({'result': 1, 'message': "该联系人已添加"})

        contact = Contact(
            name=name,
            gender=gender,
            birthdate=birthdate,
            id_card=id_card,
            user=user,
        )

        contact.save()

        return json.response({'result': 0, 'message': "添加联系人成功"})


class ContactIdView(APIView):
    @permission_check(['Common User'], user=True)
    def delete(self, request, contact_id, user):
        contact = user.contacts.filter(id=contact_id).first()

        if not contact:
            return json.response({'result': 1, 'message': "未找到联系人"})

        try:
            contact.delete()
        except RestrictedError:
            return json.response({'result': 1, 'message': "该联系人已经被用于购买车票，无法删除"})

        return json.response({'result': 0, 'message': "成功删除联系人"})

