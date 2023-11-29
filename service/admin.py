from django.contrib import admin

from service.models import Motorcycle, MotoType, MotoCompany, MotoModel


@admin.register(Motorcycle)
class MotorcycleAdmin(admin.ModelAdmin):
    pass


@admin.register(MotoType)
class MotoTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(MotoCompany)
class MotoCompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(MotoModel)
class MotoModelAdmin(admin.ModelAdmin):
    pass
