from datetime import datetime, timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView

from schedules.models import ScheduleToCarriage, Station
from tickets.models import Ticket
from tickets.serializers import TicketSerializer
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
        ori_station_id = request.data.get('ori_station_id', None)
        dst_station_id = request.data.get('dst_station_id', None)
        only_get_price = request.query_params.get('only_get_price', 'false') == 'true'

        if not schedule_id or not contact_id or not carriage_id or not ori_station_id or not dst_station_id:
            return json.response({'result': 1, 'message': "需要包含行程、联系人、座位类型和起终站点信息"})
        
        schedule2carriage = ScheduleToCarriage.objects.filter(schedule_id=schedule_id, carriage_id=carriage_id).first()

        if not schedule2carriage:
            return json.response({'result': 1, 'message': "未找到行程与对应的座位组合"})
        
        ori_station = Station.objects.filter(id=ori_station_id).first()
        dst_station = Station.objects.filter(id=dst_station_id).first()

        if not ori_station or not dst_station:
            return json.response({'result': 1, 'message': "未找到起终站点"})
        
        if not schedule2carriage.schedule.is_option_schedule(ori_station, dst_station):
            return json.response({'result': 1, 'message': "该行程和起终站点不匹配"})

        with transaction.atomic():  # must guarantee that tickets number won't change after check
            max_seat, now_seat = schedule2carriage.get_seat_info()

            if now_seat >= max_seat:
                return json.response({'result': 1, 'message': "该类座位已满"})

            contact = user.contacts.filter(id=contact_id).first()

            if not contact:
                return json.response({'result': 1, 'message': "未找到联系人"})

            amount = schedule2carriage.calc_cost(ori_station, dst_station)

            if only_get_price:
                if amount is not None:
                    return json.response({'result': 0, 'message': "获得金额成功", 'price': amount})
                else:
                    return json.response({'result': 1, 'message': "获得金额失败", 'price': amount})

            ticket = Ticket(
                amount=amount,
                seat_no=now_seat,
                schedule=schedule2carriage.schedule,
                carriage=schedule2carriage.carriage,
                contact=contact,
                user=user,
                ori_station=ori_station,
                dst_station=dst_station,
            )
            ticket.save()

            return json.response({'result': 0, 'message': "订票成功，请支付订单", 'ticket_id': ticket.id})


class TicketIdView(APIView):
    @permission_check(['Common User'], user=True)
    def get(self, request, ticket_id, user):
        """
        get ticket by id
        """
        ticket = user.tickets.filter(id=ticket_id).first()

        if not ticket:
            return json.response({'result': 1, 'message': "车票未找到"})

        return json.response(TicketSerializer(ticket).data)

    @permission_check(['Common User'], user=True)
    def put(self, request, ticket_id, user):
        """
        change ticket
        """
        new_schedule_id = request.data.get('new_schedule_id', None)
        carriage_id = request.data.get('carriage_id', None)

        if not new_schedule_id or not carriage_id:
            return json.response({'result': 1, 'message': "改签必须指定目标车票和座位号"})
        
        new_schedule2carriage = ScheduleToCarriage.objects.filter(schedule_id=new_schedule_id, carriage_id=carriage_id).first()

        if not new_schedule2carriage:
            return json.response({'result': 1, 'message': "未找到与改签行程与对应的座位组合"})

        ticket = user.tickets.filter(id=ticket_id).first()

        if not ticket:
            return json.response({'result': 1, 'message': "车票未找到"})

        if not ticket.is_schedule_modified and not ticket.is_changeable():
            return json.response({'result': 1, 'message': "该车票不可改签"})

        if not new_schedule2carriage.schedule.is_option_schedule(ticket.ori_station, ticket.dst_station):
            return json.response({'result': 1, 'message': "改签行程必须和原行程起始点相同"})

        if ticket.schedule and new_schedule2carriage.schedule.departure_time > ticket.schedule.departure_time + timedelta(hours=24):
            return json.response({'result': 1, 'message': "改签的新时间不能超过原始时间的24小时"})

        with transaction.atomic():  # must guarantee that tickets number won't change after check
            max_seat, now_seat = new_schedule2carriage.get_seat_info()

            if now_seat >= max_seat:
                return json.response({'result': 1, 'message': "该类座位已满"})

            amount = new_schedule2carriage.calc_cost(ticket.ori_station, ticket.dst_station)

            ticket.create_time = timezone.now()
            ticket.seat_no = now_seat
            ticket.schedule = new_schedule2carriage.schedule
            ticket.carriage = new_schedule2carriage.carriage
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
        account_id = request.data.get('account_id', None)
        ticket = user.tickets.filter(id=ticket_id).first()

        if not ticket:
            return json.response({'result': 1, 'message': "订单未找到"})
        
        if ticket.is_deletable():
            ticket.delete()
            return json.response({'result': 0, 'message': "订单已删除"})

        if ticket.is_cancelable():
            if not account_id:
                return json.response({'result': 1, 'message': "取消车票必须选择退款账户"})

            account = user.accounts.filter(id=account_id).first()

            if not account:
                return json.response({'result': 1, 'message': "未找到账户"})
            
            account.amount += ticket.amount
            account.save()
            ticket.delete()

            return json.response({'result': 0, 'message': "订单已取消"})

        return json.response({'result': 1, 'message': "订单不可取消" if ticket.is_paid else "订单不可删除"})
