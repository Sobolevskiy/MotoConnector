from django.contrib import admin
from django.contrib.gis import admin

from motomap.models import Place, PlaceTag, Landscape


@admin.register(Place)
class PointAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'location')


@admin.register(PlaceTag)
class PlaceTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'verified')


@admin.register(Landscape)
class LandscapeAdmin(admin.ModelAdmin):
    list_display = ('name',)
