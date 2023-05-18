from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=32)
    card_id = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='accounts')
