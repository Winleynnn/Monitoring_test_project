from django.contrib import admin
from .models import Data
# Register your models here.
@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ('id','date', 'air_temp_avg', 'relative_humidity_avg', 'soil_temp_avg', 'soil_moisture')

