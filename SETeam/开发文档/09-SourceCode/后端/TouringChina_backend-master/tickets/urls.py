from django.urls import path

from tickets import views

urlpatterns = [
    path("<int:ticket_id>", views.TicketIdView.as_view()),
    path("", views.TicketView.as_view()),
]
