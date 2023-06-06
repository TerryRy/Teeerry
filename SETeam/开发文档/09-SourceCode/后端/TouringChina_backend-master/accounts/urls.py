from django.urls import path

from accounts import views

urlpatterns = [
    path("<int:account_id>", views.AccountIdView.as_view()),
    path("", views.AccountView.as_view()),
]
