from django.db import models


# Create your models here.
class Data(models.Model):
    date = models.DateTimeField(null=True)
    air_temp_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    relative_humidity_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    soil_temp_avg = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    soil_moisture = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.date

def ass():
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
    apiRoute = '/data/0020CF3B/hourly/last/4m'
    #apiRoute = '/station/0020CF3B/sensors'

    auth = AuthHmacMetosGet(apiRoute, publicKey, privateKey)
    response = requests.get(apiURI+apiRoute, headers={'Accept': 'application/json'}, auth=auth)

    data = response.json()

    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

    dates = data['dates']
    main_data = data['data']

    for data in main_data:
        if data['name'] == 'HC Air temperature':
            air_t = data
        if data['name'] == 'HC Relative humidity':
            humidity = data
        if data['name'] == 'Soil temperature 1':
            soil_t = data
        if data['name'] == 'EAG Soil moisture 1':
            soil_moisture = data

    # air_temperature_min = air_t['values']['min']
    # air_temperature_max = air_t['values']['max']
    air_temperature_avg = air_t['values']['avg']

    # relative_humidity_min = humidity['values']['min']
    # relative_humidity_max = humidity['values']['max']
    relative_humidity_avg = humidity['values']['avg']

    # soil_temperature_min = soil_t['values']['min']
    # soil_temperature_max = soil_t['values']['max']
    soil_temperature_avg = soil_t['values']['avg']

    # soil_moisture_min = soil_moisture['values']['min']
    # soil_moisture_max = soil_moisture['values']['max']
    soil_moisture_avg = soil_moisture['values']['avg']

    # with open('data.csv', mode="w+", encoding='cp1251') as csvfile:
    #     writer = csv.writer(csvfile, delimiter=',', lineterminator="\r")
    #     writer.writerow(['Date', 'Air Temperature', 'Relative Humidity', 'Soil Temperature', 'Soil Moisture'])
    #     for i in range(1, len(air_t['values']['avg'])):
    #         writer.writerow([dates[i], air_temperature_avg[i], relative_humidity_avg[i], soil_temperature_avg[i], soil_moisture_avg[i]])
    for i in range(1, len(air_t['values']['avg'])):
        if ((air_temperature_avg[i] != None) & (relative_humidity_avg[i] != None) & (soil_temperature_avg[i] != None) & (soil_moisture_avg[i] != None)):
            Data.objects.create(date=dates[i], air_temp_avg=air_temperature_avg[i], relative_humidity_avg=relative_humidity_avg[i], soil_temp_avg=soil_temperature_avg[i], soil_moisture=soil_moisture_avg[i])

#ass()
