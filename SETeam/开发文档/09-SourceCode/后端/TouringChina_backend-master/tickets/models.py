from datetime import timedelta, datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from contacts.models import Contact
from schedules.models import Schedule, Carriage, Station


# Create your models here.
class Ticket(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    create_time = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    is_schedule_modified = models.BooleanField(default=False)
    seat_no = models.IntegerField()

    schedule = models.ForeignKey(to=Schedule, on_delete=models.SET_NULL, null=True, related_name='tickets')
    carriage = models.ForeignKey(to=Carriage, on_delete=models.CASCADE)
    ori_station = models.ForeignKey(to=Station, on_delete=models.RESTRICT, null=True, related_name='tickets_as_ori')
    dst_station = models.ForeignKey(to=Station, on_delete=models.RESTRICT, null=True, related_name='tickets_as_dst')

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='tickets')
    contact = models.ForeignKey(to=Contact, on_delete=models.RESTRICT, related_name='tickets')

    def is_expired(self):
        return not self.is_paid and (self.create_time + timedelta(days=1)) < timezone.now()

    def is_deletable(self):
        return not self.is_paid or self.is_expired()

    def is_cancelable(self):
        return self.is_paid and timezone.now() + timedelta(hours=1) < self.schedule.departure_time

    def is_changeable(self):
        return self.is_paid and timezone.now() + timedelta(days=1) < self.schedule.departure_time
