from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    UNKNOWN = "U", "Unknown"


class Contact(models.Model):
    name = models.CharField(max_length=32)
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.UNKNOWN)
    birthdate = models.DateField()
    id_card = models.CharField(max_length=32, unique=True)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='contacts')
