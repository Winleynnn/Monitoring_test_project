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
        
# def jena_gallipoli():
#     with open('jena_climate_2009_2016.csv', encoding='utf-8') as jena_file:
#         reader = csv.reader(jena_file, delimiter=',')
#         next(reader, None)
#         for row in reader:
#             #date p T Tpot Tdew rh VPmax VPact VPdef sh H2OC rho wv max_wv wd
#              Station_Jena.objects.create(date=row[0], p=row[1], T=row[2], Tpot=row[3], 
#              Tdew=row[4], rh=row[5], VPmax=row[6], VPact=row[7], VPdef=row[8], sh=row[9], 
#              H2OC=row[10], rho=row[11], wv=row[12], max_wv=row[13], wd=row[14])
#     with open('Hourly Weather Data in Gallipoli (2008-2021).csv', encoding='utf-8') as gal_file:
#         reader = csv.reader(gal_file, delimiter=';')
#         next(reader, None)
#         for row in reader:
#             # date temp sunshine short_rad relative_humidity mean_sea_pressure soil_temp soil_moisture wind_speed wind_direction
#              Station_Gallipoli.objects.create(date=row[0], sunshine=row[1], short_rad=row[2], relative_humidity=row[3], 
#              mean_sea_pressure=row[4], soil_temp=row[5], soil_moisture=row[6], wind_speed=row[7], wind_direction=row[8])

# jena_gallipoli()

def get_station_info():
    # login/pass: demo_api/demo4
    import re
    import requests
    import json
    import csv
    import sqlite3
    from requests.auth import AuthBase
    from Crypto.Hash import HMAC
    from Crypto.Hash import SHA256
    from datetime import datetime
    from dateutil.tz import tzlocal

    # Class to perform HMAC encoding
    class AuthHmacMetosGet(AuthBase):
        # Creates HMAC authorization header for Metos REST service GET request.
        def __init__(self, apiRoute, publicKey, privateKey):
            self._publicKey = publicKey
            self._privateKey = privateKey
            self._method = 'GET'
            self._apiRoute = apiRoute

        def __call__(self, request):
            dateStamp = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
            print("timestamp: ", dateStamp)
            request.headers['Date'] = dateStamp
            msg = (self._method + self._apiRoute + dateStamp + self._publicKey).encode(encoding='utf-8')
            h = HMAC.new(self._privateKey.encode(encoding='utf-8'), msg, SHA256)
            signature = h.hexdigest()
            request.headers['Authorization'] = 'hmac ' + self._publicKey + ':' + signature
            return request


    # Endpoint of the API, version for example: v1
    apiURI = 'https://api.fieldclimate.com/v2'

    # HMAC Authentication credentials
    publicKey = 'b980abf346a6dc2b8a7c91a296e02cd11316618f741f93e5'
    privateKey = '1d20cd076c1dd12ec8519ca5d05160a4236f1062c5b13235'

    # Service/Route that you wish to call
    # apiRoute = '/data/0020CF3B/hourly/last/4m'

    # auth = AuthHmacMetosGet(apiRoute, publicKey, privateKey)
    # response = requests.get(apiURI+apiRoute, headers={'Accept': 'application/json'}, auth=auth)

    # data = response.json()

    # with open('data.txt', 'w') as outfile:
    #     json.dump(data, outfile)

    # dates = data['dates']
    # main_data = data['data']

    # for data in main_data:
    #     if data['name'] == 'HC Air temperature':
    #         air_t = data
    #     if data['name'] == 'HC Relative humidity':
    #         humidity = data
    #     if data['name'] == 'Soil temperature 1':
    #         soil_t = data
    #     if data['name'] == 'EAG Soil moisture 1':
    #         soil_moisture = data

    # air_temperature_avg = air_t['values']['avg']
    # relative_humidity_avg = humidity['values']['avg']
    # soil_temperature_avg = soil_t['values']['avg']
    # soil_moisture_avg = soil_moisture['values']['avg']

    # # with open('data.csv', mode="w+", encoding='cp1251') as csvfile:
    # #     writer = csv.writer(csvfile, delimiter=',', lineterminator="\r")
    # #     writer.writerow(['Date', 'Air Temperature', 'Relative Humidity', 'Soil Temperature', 'Soil Moisture'])
    # #     for i in range(1, len(air_t['values']['avg'])):
    # #         writer.writerow([dates[i], air_temperature_avg[i], relative_humidity_avg[i], soil_temperature_avg[i], soil_moisture_avg[i]])
    # for i in range(1, len(air_t['values']['avg'])):
    #     if ((air_temperature_avg[i] != None) & (relative_humidity_avg[i] != None) & (soil_temperature_avg[i] != None) & (soil_moisture_avg[i] != None)):
    #         Station_0020CF3B.objects.create(date=dates[i], air_temp_avg=air_temperature_avg[i], relative_humidity_avg=relative_humidity_avg[i], soil_temp_avg=soil_temperature_avg[i], soil_moisture=soil_moisture_avg[i])

    # apiRoute = '/data/002099C5/hourly/last/4m'
    # auth = AuthHmacMetosGet(apiRoute, publicKey, privateKey)
    # response = requests.get(apiURI+apiRoute, headers={'Accept': 'application/json'}, auth=auth)
    # data = response.json()

    # dates = data['dates']
    # main_data = data['data']

    # for data in main_data:
    #     if data['name'] == 'HC Air temperature':
    #         air_t = data
    #     if data['name'] == 'HC Relative humidity':
    #         humidity = data
    #     if data['name'] == 'Soil temperature 1':
    #         soil_t_1 = data
    #     if data['name'] == 'Soil temperature 2':
    #         soil_t_2 = data
    #     if data['name'] == 'Soil temperature 3':
    #         soil_t_3 = data

    # air_temp = air_t['values']['avg']
    # rel_hum = humidity['values']['avg']
    # s_t_1 = soil_t_1['values']['avg']
    # s_t_2 = soil_t_2['values']['avg']
    # s_t_3 = soil_t_3['values']['avg']

    # for i in range(1, len(air_t['values']['avg'])):
    #     if ((air_temp[i] != None) & (rel_hum[i] != None) & (s_t_1[i] != None) & (s_t_2[i] != None) & (s_t_3[i] != None)):
    #         Station_002099C5.objects.create(date=dates[i], air_temp_avg=air_temp[i], relative_humidity_avg=rel_hum[i], soil_temp_1=s_t_1[i], soil_temp_2=s_t_2[i], soil_temp_3=s_t_3[i])

    apiRoute = '/data/00000235/hourly/last/4m'
    auth = AuthHmacMetosGet(apiRoute, publicKey, privateKey)
    response = requests.get(apiURI+apiRoute, headers={'Accept': 'application/json'}, auth=auth)
    data = response.json()

    # 00000235: id, date, air_temp_avg, relative_humidity_avg, dew_point, wind_speed_avg, wind_speed_max

    dates = data['dates']
    main_data = data['data']

    for data in main_data:
        if data['name'] == 'HC Air temperature':
            air_t = data
        if data['name'] == 'HC Relative humidity':
            humidity = data
        if data['name'] == 'Dew Point':
            dew_point = data
        if data['name'] == 'Wind speed':
            wind_speed_avg = data
        if data['name'] == 'Wind speed max':
            wind_speed_max = data

    air_temp = air_t['values']['avg']
    rel_hum = humidity['values']['avg']
    dew_p = dew_point['values']['avg']
    wind_avg = wind_speed_avg['values']['avg']
    row = wind_speed_max['values']['max']

    for i in range(1, len(air_t['values']['avg'])):
        if ((air_temp[i] != None) & (rel_hum[i] != None) & (dew_p[i] != None) & (wind_avg[i] != None) & (row[i] != None)):
            Station_00000235.objects.create(date=dates[i], air_temp_avg=air_temp[i], relative_humidity_avg=rel_hum[i], dew_point=dew_p[i], wind_speed_avg=wind_avg[i], wind_speed_max=row[i])

# get_station_info()
