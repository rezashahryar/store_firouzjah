from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.Staff)
class StaffAdmin(admin.ModelAdmin):
    
    fieldsets = (
        # ('group permissions', {
        #     'fields': (
        #         'staff_permissions', 'groups',
        #     )
        # }),
        # ('group permissions', {
        #     'fields': (
        #         'groups',
        #     )
        # }),
    )
