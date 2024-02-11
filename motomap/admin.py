from django.contrib.gis import admin

from motomap.models import Place, PlaceTag, Landscape, PlaceImage


class PlaceImageInline(admin.StackedInline):
    model = PlaceImage
    can_delete = True
    extra = 1


@admin.register(Place)
class PlaceAdmin(admin.OSMGeoAdmin):
    inlines = [PlaceImageInline]
    list_display = ('name', 'location')


@admin.register(PlaceTag)
class PlaceTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'verified')


@admin.register(Landscape)
class LandscapeAdmin(admin.ModelAdmin):
    list_display = ('name',)
