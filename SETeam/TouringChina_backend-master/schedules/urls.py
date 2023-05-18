from django.urls import path

from schedules import views

urlpatterns = [
    path("stations", views.StationView.as_view()),
    path("carriages", views.CarriageView.as_view()),
    path("<int:schedule_id>", views.ScheduleIdView.as_view()),
    path("", views.ScheduleView.as_view()),
]
