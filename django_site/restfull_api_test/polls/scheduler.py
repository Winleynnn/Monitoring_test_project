from django.db import models
from polls.models import Station_00000235, Station_002099C5, Station_0020CF3B
import requests
from requests.auth import AuthBase
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
from datetime import datetime
from dateutil.tz import tzlocal
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler



# login/pass: demo_api/demo4
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
publicKey = '390cf046de64c36802b3d85cbf1883bf1294fe919549a3fe'
privateKey = '838e76d236581a4776b2e4b0f712c6ebc1c7789f32af7aca'

def station_0020CF3B_update():
    apiRoute = '/data/0020CF3B/hourly/last/1d'

    auth = AuthHmacMetosGet(apiRoute, publicKey, privateKey)
    response = requests.get(apiURI+apiRoute, headers={'Accept': 'application/json'}, auth=auth)

    data = response.json()

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

    air_temperature_avg = air_t['values']['avg']
    relative_humidity_avg = humidity['values']['avg']
    soil_temperature_avg = soil_t['values']['avg']
    soil_moisture_avg = soil_moisture['values']['avg']

    # with open('data.csv', mode="w+", encoding='cp1251') as csvfile:
    #     writer = csv.writer(csvfile, delimiter=',', lineterminator="\r")
    #     writer.writerow(['Date', 'Air Temperature', 'Relative Humidity', 'Soil Temperature', 'Soil Moisture'])
    #     for i in range(1, len(air_t['values']['avg'])):
    #         writer.writerow([dates[i], air_temperature_avg[i], relative_humidity_avg[i], soil_temperature_avg[i], soil_moisture_avg[i]])
    for i in range(1, len(air_t['values']['avg'])):
        if ((air_temperature_avg[i] != None) & (relative_humidity_avg[i] != None) & (soil_temperature_avg[i] != None) & (soil_moisture_avg[i] != None)):
            Station_0020CF3B.objects.create(date=dates[i], air_temp_avg=air_temperature_avg[i], relative_humidity_avg=relative_humidity_avg[i], soil_temp_avg=soil_temperature_avg[i], soil_moisture=soil_moisture_avg[i])

    print('Update for last hour on 0020CF3B complete')


def station_002099C5_update():
    apiRoute = '/data/002099C5/hourly/last/1d'
    auth = AuthHmacMetosGet(apiRoute, publicKey, privateKey)
    response = requests.get(apiURI+apiRoute, headers={'Accept': 'application/json'}, auth=auth)
    data = response.json()

    dates = data['dates']
    main_data = data['data']

    for data in main_data:
        if data['name'] == 'HC Air temperature':
            air_t = data
        if data['name'] == 'HC Relative humidity':
            humidity = data
        if data['name'] == 'Soil temperature 1':
            soil_t_1 = data
        if data['name'] == 'Soil temperature 2':
            soil_t_2 = data
        # if data['name'] == 'Soil temperature 3':
        #     soil_t_3 = data

    air_temp = air_t['values']['avg']
    rel_hum = humidity['values']['avg']
    s_t_1 = soil_t_1['values']['avg']
    s_t_2 = soil_t_2['values']['avg']
    # s_t_3 = soil_t_3['values']['avg']

    for i in range(1, len(air_t['values']['avg'])):
        if ((air_temp[i] != None) & (rel_hum[i] != None) & (s_t_1[i] != None) & (s_t_2[i] != None)):
            Station_002099C5.objects.create(date=dates[i], air_temp_avg=air_temp[i], relative_humidity_avg=rel_hum[i], soil_temp_1=s_t_1[i], soil_temp_2=s_t_2[i])

    print('Update for last hour on 002099C5 complete')

def station_00000235_update():
    apiRoute = '/data/00000235/hourly/last/1d'
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

    print('Update for last hour on 00000235 complete')

def get_station_info():
    station_00000235_update()
    station_002099C5_update()
    station_0020CF3B_update()

def start():
    print('hello')
    # get_station_info()
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(get_station_info, 'interval', hours=1)
    # scheduler.start()
