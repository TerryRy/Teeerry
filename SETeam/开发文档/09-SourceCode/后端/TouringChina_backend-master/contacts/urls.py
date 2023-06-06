from django.urls import path

from contacts import views

urlpatterns = [
    path("<int:contact_id>", views.ContactIdView.as_view()),
    path("", views.ContactView.as_view()),
]
