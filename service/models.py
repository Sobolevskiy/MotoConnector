import secrets
from datetime import datetime, timezone

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User


class CommonCatalog(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        abstract = True


class MotoType(CommonCatalog):
    pass


class MotoCompany(CommonCatalog):
    pass


class MotoModel(CommonCatalog):
    pass


class Motorcycle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    moto_type = models.ForeignKey(MotoType, on_delete=models.CASCADE)
    moto_company = models.ForeignKey(MotoCompany, on_delete=models.CASCADE)
    moto_model = models.ForeignKey(MotoModel, on_delete=models.CASCADE)
