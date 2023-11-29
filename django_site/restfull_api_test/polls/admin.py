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

@admin.register(Station_Jena)
class Station_Jena_Admin(admin.ModelAdmin):
    #date p T Tpot Tdew rh VPmax VPact VPdef sh H2OC rho wv max_wv wd
    list_display = ('id','date', 'p', 'T', 'Tpot', 'Tdew', 'rh', 'VPmax', 'VPact', 'VPdef', 'sh', 'H2OC', 'rho', 'wv', 'max_wv', 'wd')

@admin.register(Station_Gallipoli)
class Station_Gallipoli_Admin(admin.ModelAdmin):
     # date temp sunshine short_rad relative_humidity mean_sea_pressure soil_temp soil_moisture wind_speed wind_direction
    list_display = ('id','date', 'temp', 'sunshine', 'short_rad', 'relative_humidity', 'mean_sea_pressure', 'soil_temp', 'soil_moisture', 'wind_speed', 'wind_direction')

@admin.register(User_Models)
class User_Models_Admin(admin.ModelAdmin):
    list_display = ('login', 'station_id')