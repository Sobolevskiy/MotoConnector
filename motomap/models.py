from django import forms
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from socials.models import Commentable


class _TypedMultipleChoiceField(forms.TypedMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs.pop("base_field", None)
        kwargs.pop("max_length", None)
        super().__init__(*args, **kwargs)


class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': _TypedMultipleChoiceField,
            'choices': self.base_field.choices,
            'coerce': self.base_field.to_python,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't care for it.
        # pylint:disable=bad-super-call
        return super().formfield(**defaults)


class PlaceTag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}./.{self.verified}"


class Landscape(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Place(Commentable, models.Model):
    NATURE_TYPE = 100
    HISTORIC_TYPE = 200
    MAN_MADE_TYPE = 300
    PLACE_TYPES_CHOICES = (
        (NATURE_TYPE, 'Природное'),
        (HISTORIC_TYPE, 'Историческое'),
        (MAN_MADE_TYPE, 'Техногенное'),
    )

    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    place_type = ChoiceArrayField(
        models.IntegerField(choices=PLACE_TYPES_CHOICES, default=NATURE_TYPE)
    )
    geometry = models.PointField()
    tags = models.ManyToManyField(PlaceTag, related_name="tags", blank=True)
    landscapes = models.ManyToManyField(Landscape, related_name="landscapes", blank=True)
    discoverer = models.ForeignKey(User, related_name="places", on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PlaceImage(models.Model):
    image = models.ImageField(upload_to='places', null=True, blank=True)
    place = models.ForeignKey(Place, related_name='images', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(pre_delete, sender=PlaceImage)
def place_image_delete(sender, instance, **kwargs):
    instance.image.delete(False)
