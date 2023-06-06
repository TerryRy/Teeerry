from rest_framework import serializers

from schedules.models import Station, Carriage, ScheduleToCarriage, Schedule, ScheduleToStation


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = "__all__"


class CarriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carriage
        fields = "__all__"


class ScheduleToCarriageSerializer(serializers.ModelSerializer):
    carriage = CarriageSerializer()
    rest_seats = serializers.SerializerMethodField()

    class Meta:
        model = ScheduleToCarriage
        fields = ['carriage', 'num', 'rest_seats']

    def get_rest_seats(self, obj):
        max_seat, now_seat = obj.get_seat_info()
        return max_seat - now_seat


class ScheduleToStationSerializer(serializers.ModelSerializer):
    station = StationSerializer()
    arrival_time = serializers.DateTimeField()

    class Meta:
        model = ScheduleToStation
        fields = ['station', 'order', 'arrival_time']


class ScheduleSerializer(serializers.ModelSerializer):
    carriages = serializers.SerializerMethodField()
    stations = serializers.SerializerMethodField()
    departure_time = serializers.DateTimeField()

    class Meta:
        model = Schedule
        fields = ['id', 'schedule_no', 'departure_time', 'stations', 'carriages']

    def get_carriages(self, obj):
        carriages = ScheduleToCarriage.objects.filter(schedule=obj)
        return ScheduleToCarriageSerializer(carriages, many=True).data

    def get_stations(self, obj):
        stations = ScheduleToStation.objects.filter(schedule=obj)
        return ScheduleToStationSerializer(stations, many=True).data
