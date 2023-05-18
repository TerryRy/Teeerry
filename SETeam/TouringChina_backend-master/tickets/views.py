from datetime import datetime

from rest_framework.views import APIView

from schedules.models import Schedule
from tickets.models import Ticket
from tickets.serializers import TicketSerializer
from tickets.utils import calc_cost, get_seat_info
from utils import json
from utils.perm import permission_check


# Create your views here.
class TicketView(APIView):
    @permission_check(['Common User'], user=True)
    def get(self, request, user):
        """
        list all ticket of user
        """
        return json.response({'tickets': TicketSerializer(user.tickets.all(), many=True).data})

    @permission_check(['Common User'], user=True)
    def post(self, request, user):
        """
        let user buy a ticket
        """
        schedule_id = request.data.get('schedule_id', None)
        contact_id = request.data.get('contact_id', None)
        carriage_id = request.data.get('carriage_id', None)

        if not schedule_id or not contact_id or not carriage_id:
            return json.response({'result': 1, 'message': "需要包含行程、联系人和座位类型"})

        if not user.contacts.filter(id=contact_id).exists():
            return json.response({'result': 1, 'message': "未找到联系人"})

        contact = user.contacts.get(id=contact_id)

        schedule = Schedule.objects.filter(id=schedule_id).first()

        if not schedule:
            return json.response({'result': 1, 'message': "未找到行程"})

        carriage = schedule.carriages.filter(id=carriage_id).first()

        if not carriage:
            return json.response({'result': 1, 'message': "未找到座位类型"})

        max_seat, now_seat = get_seat_info(schedule, carriage)

        if now_seat >= max_seat:
            return json.response({'result': 1, 'message': "该类座位已满"})

        amount = calc_cost(schedule.stations.count(), carriage.increase_rate)

        ticket = Ticket(
            amount=amount,
            seat_no=now_seat,
            schedule=schedule,
            carriage=carriage,
            contact=contact,
            user=user,
        )
        ticket.save()

        return json.response({'result': 0, 'message': "订票成功，请支付订单"})


class TicketIdView(APIView):
    @permission_check(['Common User'], user=True)
    def put(self, request, ticket_id, user):
        """
        change ticket
        """
        new_schedule_id = request.data.get('new_schedule_id', None)
        carriage_id = request.data.get('carriage_id', None)

        if not new_schedule_id or not carriage_id:
            return json.response({'result': 1, 'message': "改签必须指定目标车票和座位号"})

        new_schedule = Schedule.objects.filter(id=new_schedule_id).first()

        if not new_schedule:
            return json.response({'result': 1, 'message': "行程未找到"})

        new_carriage = new_schedule.carriages.filter(id=carriage_id).first()

        if not new_carriage:
            return json.response({'result': 1, 'message': "座位未找到"})

        ticket = user.tickets.filter(id=ticket_id).first()

        if not ticket:
            return json.response({'result': 1, 'message': "车票未找到"})

        if not ticket.is_schedule_modified and not ticket.is_changeable():
            return json.response({'result': 1, 'message': "该车票不可改签"})

        if not ticket.schedule.is_option_schedule(new_schedule):
            return json.response({'result': 1, 'message': "改签行程必须和原行程起始点相同"})

        max_seat, now_seat = get_seat_info(new_schedule, new_carriage)

        if now_seat >= max_seat:
            return json.response({'result': 1, 'message': "该类座位已满"})

        amount = calc_cost(new_schedule.stations.count(), new_carriage.increase_rate)

        ticket.create_time = datetime.now()
        ticket.seat_no = now_seat
        ticket.schedule = new_schedule
        ticket.carriage = new_carriage
        ticket.is_schedule_modified = False

        if not ticket.is_schedule_modified:
            ticket.is_paid = False
            ticket.amount = amount - ticket.amount

        ticket.save()

        return json.response({'result': 0, 'message': "车票已改签"})

    @permission_check(['Common User'], user=True)
    def patch(self, request, ticket_id, user):
        """
        pay for the ticket
        """
        account_id = request.data.get('account_id', None)

        if not account_id:
            return json.response({'result': 1, 'message': "必须选择支付账户"})

        account = user.accounts.filter(id=account_id).first()

        if not account:
            return json.response({'result': 1, 'message': "未找到账户"})

        ticket = user.tickets.filter(id=ticket_id).first()

        if not ticket:
            return json.response({'result': 1, 'message': "未找到要支付的车票"})

        if ticket.is_paid:
            return json.response({'result': 1, 'message': "车票已支付"})

        if ticket.is_schedule_modified:
            return json.response({'result': 1, 'message': "所购列车行程已更改，请重新购票"})

        if ticket.is_expired():
            return json.response({'result': 1, 'message': "车票订单已过期，请删除订单"})

        if ticket.amount > account.amount:
            return json.response({'result': 1, 'message': "账户余额不足"})

        account.amount -= ticket.amount
        ticket.is_paid = True

        account.save()
        ticket.save()

        return json.response({'result': 0, 'message': "车票订单支付成功"})

    @permission_check(['Common User'], user=True)
    def delete(self, request, ticket_id, user):
        """
        delete un-payed ticket order or cancel payed ticket
        """
        ticket = user.tickets.filter(id=ticket_id).first()

        if not ticket:
            return json.response({'result': 1, 'message': "订单未找到"})

        if ticket and (ticket.is_deletable() or ticket.is_deletable()):
            ticket.delete()
            return json.response({'result': 0, 'message': "订单已取消" if ticket.is_paid else "订单已删除"})

        return json.response({'result': 1, 'message': "订单不可取消" if ticket.is_paid else "订单不可删除"})
