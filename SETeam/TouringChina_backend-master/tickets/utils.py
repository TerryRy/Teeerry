import decimal

from django.conf import settings

from schedules.models import ScheduleToCarriage


def calc_cost(station_num, carriage_increase_rate):
    return decimal.Decimal(carriage_increase_rate) * (
            (decimal.Decimal(station_num) - 1) *
            settings.AVG_KM_BETWEEN_STATION *
            settings.ADDITION_COST_PER_KM
    )


def get_seat_info(schedule, carriage):
    schedule2carriage = ScheduleToCarriage.objects.get(schedule=schedule, carriage=carriage)
    max_seat = schedule2carriage.num * schedule2carriage.carriage.seat_num
    now_seat = schedule.tickets.filter(carriage=carriage).count()

    return max_seat, now_seat
