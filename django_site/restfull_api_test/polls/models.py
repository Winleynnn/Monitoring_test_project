from django.db import models
import csv

# Create your models here.
class Station_0020CF3B(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.TextField(null=True)
    air_temp_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    relative_humidity_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    soil_temp_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    soil_moisture = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.date

class Station_002099C5(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.TextField(null=True)
    air_temp_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    relative_humidity_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    soil_temp_1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    soil_temp_2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    soil_temp_3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.date

class Station_00000235(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.TextField(null=True)
    air_temp_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    relative_humidity_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dew_point = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wind_speed_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wind_speed_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.date

class Station_Gallipoli(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.TextField(null=True)
    temp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sunshine = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    short_rad = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    relative_humidity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mean_sea_pressure = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    soil_temp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    soil_moisture = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wind_speed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wind_direction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.date

class Station_Jena(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.TextField(null=True)
    p = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    T = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Tpot = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Tdew = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rh = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    VPmax = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    VPact = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    VPdef = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sh = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    H2OC = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rho = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wv = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_wv = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    wd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.date
        
class User_Models(models.Model):
    login = models.TextField(null=False)
    station_id = models.TextField(null=False)
    def __str__(self):
        return self.login
    
# def jena_gallipoli():
#     with open('jena.csv', encoding='utf-8') as jena_file:
#         reader = csv.reader(jena_file, delimiter=';')
#         next(reader, None)
#         for row in reader:
#             #date p T Tpot Tdew rh VPmax VPact VPdef sh H2OC rho wv max_wv wd
#              Station_Jena.objects.create(date=row[0], p=row[1], T=row[2], Tpot=row[3], Tdew=row[4], rh=row[5], VPmax=row[6], VPact=row[7], VPdef=row[8], sh=row[9], H2OC=row[10], rho=row[11], wv=row[12], max_wv=row[13], wd=row[14])
#     with open('gallipoli.csv', encoding='utf-8') as gal_file:
#         reader = csv.reader(gal_file, delimiter=';')
#         next(reader, None)
#         for row in reader:
#             # date temp sunshine short_rad relative_humidity mean_sea_pressure soil_temp soil_moisture wind_speed wind_direction
#              Station_Gallipoli.objects.create(date=row[0], sunshine=row[1], short_rad=row[2], relative_humidity=row[3], mean_sea_pressure=row[4], soil_temp=row[5], soil_moisture=row[6], wind_speed=row[7], wind_direction=row[8])

# jena_gallipoli()

