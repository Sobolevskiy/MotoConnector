from django import forms
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField


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


class Place(models.Model):
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
    location = models.PointField()

    def __str__(self):
        return self.name
