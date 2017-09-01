# coding=utf-8
from django.contrib import admin

from .models import Person, Department, Position


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass
