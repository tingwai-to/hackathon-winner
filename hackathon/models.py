from django.db import models


class Subscription(models.Model):
    email = models.EmailField(primary_key=True, unique=True)
    frequency = models.IntegerField(default=0)