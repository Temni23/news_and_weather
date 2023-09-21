from django.contrib import admin
from django_admin_geomap import ModelAdmin
from .models import Place


class PlaceAdmin(ModelAdmin):
    list_display = ['id', 'name', 'lon', 'lat', 'rating']
    list_editable = ['name', 'rating']
    geomap_field_longitude = 'id_lon'
    geomap_field_latitude = 'id_lat'
    geomap_height = '400px'
    geomap_default_zoom = '1'


admin.site.register(Place, PlaceAdmin)
