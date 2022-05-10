from django.contrib import admin

from RadioUniverse.models import RadioStation


@admin.register(RadioStation)
class RadioStationAdmin(admin.ModelAdmin):
    list_filter = ['country',]
    list_display = ['name', 'url', 'country']
