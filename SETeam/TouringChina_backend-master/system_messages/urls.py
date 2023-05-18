from django.urls import path

from system_messages import views

urlpatterns = [
    path("<int:message_id>", views.MessageIdView.as_view()),
    path("", views.MessageView.as_view()),
]
