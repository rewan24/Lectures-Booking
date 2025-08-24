from django.contrib import admin
from .models import Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'schedule', 'days']
    filter_horizontal = ['students']