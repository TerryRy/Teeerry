from rest_framework import serializers

from contacts.serializers import ContactSerializer
from schedules.models import Carriage, Schedule
from schedules.serializers import StationSerializer
from tickets.models import Ticket


class CarriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carriage
        fields = ['id', 'name']


class ScheduleSerializer(serializers.ModelSerializer):
    departure_station = serializers.SerializerMethodField()
    destination_station = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['id', 'schedule_no', 'departure_time', 'departure_station', 'destination_station']

    def get_departure_station(self, obj):
        return StationSerializer(obj.stations.first()).data

    def get_destination_station(self, obj):
        return StationSerializer(obj.stations.last()).data


class TicketSerializer(serializers.ModelSerializer):
    is_expired = serializers.SerializerMethodField()
    schedule = ScheduleSerializer()
    carriage = CarriageSerializer()
    contact = ContactSerializer()
    ori_station = StationSerializer()
    dst_station = StationSerializer()

    class Meta:
        model = Ticket
        exclude = ['user']

    def get_is_expired(self, obj):
        return obj.is_expired()
