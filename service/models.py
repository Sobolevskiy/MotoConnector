from django.db import models
from django.contrib.auth.models import User


class MotoType(models.Model):
    name = models.CharField(max_length=64)


class Motorcycle(models.Model):
    LOW_CC = 0
    MIDDLE_CC = 10
    MIDDLE_UP_CC = 20
    UP_CC = 30
    HIGH_CC = 40

    CC_CHOICES = (
        (LOW_CC, '0-200'),
        (MIDDLE_CC, '200-500'),
        (MIDDLE_UP_CC, '500-700'),
        (UP_CC, '700-1000'),
        (HIGH_CC, '>1000'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    moto_type = models.ForeignKey(MotoType, on_delete=models.CASCADE)
    cc = models.IntegerField(choices=CC_CHOICES, default=LOW_CC)
