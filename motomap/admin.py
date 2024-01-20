from django.contrib import admin
from django.contrib.gis import admin

from motomap.models import Place


@admin.register(Place)
class PointAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'location')
    