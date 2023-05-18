from rest_framework import serializers

from contacts.serializers import ContactSerializer
from schedules.models import Carriage, Schedule
from tickets.models import Ticket


class CarriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carriage
        fields = ['id', 'name']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'schedule_no', 'departure_time']


class TicketSerializer(serializers.ModelSerializer):
    is_expired = serializers.SerializerMethodField()
    schedule = ScheduleSerializer()
    carriage = CarriageSerializer()
    contact = ContactSerializer()

    class Meta:
        model = Ticket
        exclude = ['user']

    def get_is_expired(self, obj):
        return obj.is_expired()
