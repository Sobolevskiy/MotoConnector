from django.contrib import admin

from service.models import Motorcycle, MotoType


@admin.register(Motorcycle)
class MotorcycleAdmin(admin.ModelAdmin):
    pass


@admin.register(MotoType)
class MotoTypeAdmin(admin.ModelAdmin):
    pass
