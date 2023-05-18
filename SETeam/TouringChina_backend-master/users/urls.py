from django.urls import path

from users import views

urlpatterns = [
    path("login", views.login),
    path("register", views.start_register),
    path("register/<code>", views.verify_register),
    path("<int:user_id>", views.UserIdView.as_view()),
    path("", views.UserView.as_view()),
]
