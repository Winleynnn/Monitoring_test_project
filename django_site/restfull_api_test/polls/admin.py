from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Station_0020CF3B)
class Station_0020CF3B_Admin(admin.ModelAdmin):
    list_display = ('id','date', 'air_temp_avg', 'relative_humidity_avg', 'soil_temp_avg', 'soil_moisture')

@admin.register(Station_002099C5)
class Station_002099C5_Admin(admin.ModelAdmin):
    list_display = ('id','date', 'air_temp_avg', 'relative_humidity_avg', 'soil_temp_1', 'soil_temp_2', 'soil_temp_3')

@admin.register(Station_00000235)
class Station_00000235_Admin(admin.ModelAdmin):
    list_display = ('id','date', 'air_temp_avg', 'relative_humidity_avg', 'dew_point', 'wind_speed_avg', 'wind_speed_max')