import decimal

from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountSerializer
from utils import json
from utils.perm import permission_check


# Create your views here.
class AccountView(APIView):
    @permission_check(['Common User'], user=True)
    def post(self, request, user):
        """
        add a new account for the user
        """
        account_name = request.data.get('account_name', "undefined")
        card_holder_name = request.data.get('card_holder_name', None)
        card_id = request.data.get('card_id', None)

        if card_holder_name is None or card_id is None:
            return json.response({'result': 1, 'message': "必须填写持卡人和卡号"})

        if user.accounts.filter(card_id=card_id).exists():
            return json.response({'result': 1, 'message': "该银行卡已经被添加过了"})

        # todo: need to verify account information
        #  like verify_success = verify_account(card_id, card_holder_name)
        verify_success = True
        if not verify_success:
            return json.response({'result': 1, 'message': "银行卡信息认证未通过"})

        account = Account(name=account_name, card_id=card_id, user=user)
        account.save()
        user.accounts.add(account)

        return json.response({'result': 0, 'message': "创建账户成功"})

    @permission_check(['Common User'], user=True)
    def get(self, request, user):
        """
        list all accounts for the user
        """
        return json.response({'accounts': [AccountSerializer(ac).data for ac in user.accounts.all()]})


class AccountIdView(APIView):
    @permission_check(['Common User'], user=True)
    def delete(self, request, account_id, user):
        """
        delete account by id
        """
        if not user.accounts.filter(id=account_id).exists():
            return json.response({'result': 1, 'message': "该账户不存在"})

        user.accounts.filter(id=account_id).delete()

        return json.response({'result': 0, 'message': "成功删除账户"})

    @permission_check(['Common User'], user=True)
    def put(self, request, account_id, user):
        amount = request.data.get('amount', None)

        if not user.accounts.filter(id=account_id).exists():
            return json.response({'result': 1, 'message': "该账户不存在"})

        if not amount:
            return json.response({'result': 1, 'message': "必须输入金额"})

        account = user.accounts.get(id=account_id)

        # todo: need to recharge from "bank"
        #  like recharge(account.card_id, from=USER_ACCOUNT, to=OUR_ACCOUNT)

        account.amount += decimal.Decimal(amount)
        account.save()

        return json.response({'result': 0, 'message': "充值成功"})
