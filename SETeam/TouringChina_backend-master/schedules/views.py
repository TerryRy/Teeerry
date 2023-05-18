from datetime import datetime

from rest_framework.views import APIView

from schedules.models import Schedule, Station, Carriage
from schedules.serializers import ScheduleSerializer, StationSerializer, CarriageSerializer
from system_messages.models import Message
from utils import json
from utils.perm import permission_check


# Create your views here.
class ScheduleView(APIView):
    def get(self, request):
        """
        list all train schedule
        """
        return json.response({"schedules": ScheduleSerializer(Schedule.objects.all(), many=True).data})

    @permission_check(['Train Admin'])
    def post(self, request):
        """
        add new schedule to timetable
        """
        schedule_no = request.data.get('schedule_no', None)
        station_ids = request.data.get('station_ids', None)
        carriage_ids = request.data.get('carriage_ids', None)
        departure_time = request.data.get('departure_time', None)
        arrival_times = request.data.get('arrival_times', None)

        if (not schedule_no
                or not station_ids or not carriage_ids
                or not departure_time or not arrival_times):
            return json.response({'result': 1, 'message': "必须设置行程编号、出发时间、各站点及其到达时间、车厢"})

        if Schedule.objects.filter(schedule_no=schedule_no).exists():
            return json.response({'result': 1, 'message': "行程编号已存在"})

        schedule = Schedule(schedule_no=schedule_no, departure_time=datetime.fromisoformat(departure_time))
        schedule.save()

        if len(station_ids) != len(arrival_times):
            return json.response({'result': 1, 'message': "请为每个站点设置到达时间"})

        schedule.add_stations(station_ids, arrival_times)

        schedule.add_carriages(carriage_ids)

        return json.response({'result': 0, 'message': "设置行程成功"})


class ScheduleIdView(APIView):
    @permission_check(['Train Admin'], user=True)
    def put(self, request, schedule_id, user):
        """
        modify schedule
        """
        if not Schedule.objects.filter(id=schedule_id).exists():
            return json.response({'result': 1, 'message': "行程不存在"})

        schedule = Schedule.objects.get(id=schedule_id)

        station_ids = request.data.get('station_ids', None)
        carriage_ids = request.data.get('carriage_ids', None)
        departure_time = request.data.get('departure_time', None)
        arrival_times = request.data.get('arrival_times', None)

        if station_ids and arrival_times:
            if len(station_ids) != len(arrival_times):
                return json.response({'result': 1, 'message': "请为每个站点设置到达时间"})
            schedule.stations.clear()
            schedule.add_stations(station_ids, arrival_times)

        if carriage_ids:
            schedule.carriages.clear()
            schedule.add_carriages(carriage_ids)

        if departure_time:
            schedule.departure_time = datetime.fromisoformat(departure_time)
            schedule.save()

        message = Message(
            message=f"您购买的车次”{schedule.schedule_no}“已发生修改。您可以免费改签其他车次",
            from_user=user,
        )
        message.save()

        for ticket in schedule.tickets.all():
            ticket.is_schedule_modified = True
            ticket.save()
            message.to_users.add(ticket.user)

        return json.response({'result': 0, 'message': "行程修改成功"})

    @permission_check(['Train Admin'], user=True)
    def delete(self, request, schedule_id, user):
        """
        delete schedule
        """
        schedule = Schedule.objects.filter(id=schedule_id).first()

        if not schedule:
            json.response({'result': 1, 'message': "未找到要删除的行程"})

        schedule.delete()

        message = Message(
            message=f"您购买的车次”{schedule.schedule_no}“已被取消。您可以免费改签其他车次",
            from_user=user,
        )
        message.save()

        for ticket in schedule.tickets.all():
            ticket.is_schedule_modified = True
            ticket.save()
            message.to_users.add(ticket.user)

        return json.response({'result': 0, 'message': "行程已删除"})


class StationView(APIView):
    def get(self, request):
        """
        list all stations
        """
        return json.response({'stations': StationSerializer(Station.objects.all(), many=True).data})

    @permission_check(['Train Admin'])
    def post(self, request):
        """
        add new train station
        """
        station_no = request.data.get('station_no', None)
        name = request.data.get('name', None)

        if not station_no or not name:
            return json.response({'result': 1, 'message': "必须设置站点编号和站点名"})

        if Station.objects.filter(station_no=station_no).exists():
            return json.response({'result': 1, 'message': "站点编号已存在"})

        station = Station(station_no=station_no, name=name)
        station.save()

        return json.response({'result': 0, 'message': "添加站点成功"})


class CarriageView(APIView):
    def get(self, request):
        """
        list all carriages
        """
        return json.response({'carriages': CarriageSerializer(Carriage.objects.all(), many=True).data})

    @permission_check(['Train Admin'])
    def post(self, request):
        """
        add new carriage
        """
        name = request.data.get('name', None)
        seat_num = request.data.get('seat_num', None)
        increase_rate = request.data.get('increase_rate', None)

        if not seat_num or not name:
            return json.response({'result': 1, 'message': "必须设置车厢名和车厢座位数"})

        if Carriage.objects.filter(name=name).exists():
            return json.response({'result': 1, 'message': "车厢名已存在"})

        carriage = Carriage(name=name, seat_num=seat_num)

        if increase_rate:
            carriage.increase_rate = increase_rate

        carriage.save()

        return json.response({'result': 0, 'message': "添加车厢成功"})
