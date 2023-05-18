from collections import Counter
from datetime import datetime

from django.db import models


# Create your models here.
class Schedule(models.Model):
    schedule_no = models.CharField(max_length=32, unique=True)
    departure_time = models.DateTimeField()

    stations = models.ManyToManyField(to="Station", through="ScheduleToStation")
    carriages = models.ManyToManyField(to="Carriage", through="ScheduleToCarriage")

    def add_stations(self, station_ids, arrival_times):
        for i in range(len(station_ids)):
            station_id = station_ids[i]
            arrival_time = datetime.fromisoformat(arrival_times[i])

            schedule2station = ScheduleToStation(
                schedule=self,
                station_id=station_id,
                order=i,
                arrival_time=arrival_time,
            )
            schedule2station.save()

    def add_carriages(self, carriage_ids):
        carriage_count = Counter(carriage_ids)
        for carriage_id in carriage_count:
            num = carriage_count[carriage_id]

            schedule2carriage = ScheduleToCarriage(
                schedule=self,
                carriage_id=carriage_id,
                num=num,
            )
            schedule2carriage.save()

    def is_option_schedule(self, obj):
        self_first = self.stations.first()
        self_last = self.stations.last()
        obj_first = obj.stations.first()
        obj_last = obj.stations.last()
        return self_first == obj_first and self_last == obj_last


class Station(models.Model):
    station_no = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32)


class ScheduleToStation(models.Model):
    schedule = models.ForeignKey(to="Schedule", on_delete=models.CASCADE)
    station = models.ForeignKey(to="Station", on_delete=models.CASCADE)
    order = models.IntegerField()
    arrival_time = models.DateTimeField()

    class Meta:
        ordering = ['order']


class Carriage(models.Model):
    name = models.CharField(max_length=32)
    seat_num = models.IntegerField()
    increase_rate = models.DecimalField(max_digits=10, decimal_places=2, default=1)


class ScheduleToCarriage(models.Model):
    schedule = models.ForeignKey(to="Schedule", on_delete=models.CASCADE)
    carriage = models.ForeignKey(to="Carriage", on_delete=models.CASCADE)
    num = models.IntegerField()
