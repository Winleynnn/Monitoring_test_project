from polls.models import Station_00000235, Station_002099C5, Station_0020CF3B
import requests
from requests.auth import AuthBase
from Crypto.Hash import HMAC
from Crypto.Hash import SHA256
from datetime import date, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
import os
from threading import Thread


def db_backup():
    # def mainBackup():
        print('[BACKUP] Starting backup db for ' + str(datetime.now()))
        if not os.path.exists('backups'):
            os.mkdir('backups')
        output_filename = "backups/backup_db_" + str(date.today()) + ".json"
        with open(output_filename,'w') as output:
            call_command('dumpdata', format='json',indent=2,stdout=output, exclude=['contenttypes'])
        print('[BACKUP] Backup db for ' + str(datetime.now()) + ' complete.')
    # thr1 = Thread(target=mainBackup)
    # thr1.start()

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

publicKey = '02e99bbbf3f55b76a53525e09d0ed4051cd93ae1bd5c8735'
privateKey = 'cd749d389a1150bd79b22e9fa0c60c532eda69bba4ba933e'

def station_0020CF3B_update():
    print('[UPDATE] Starting update for last 3 days on 0020CF3B.')
    apiRoute = '/data/0020CF3B/hourly/last/3d'

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
    
    count = 0
    for i in range(1, len(air_t['values']['avg'])):
        if ((air_temperature_avg[i] != None) & (relative_humidity_avg[i] != None) & (soil_temperature_avg[i] != None) & (soil_moisture_avg[i] != None)):
            timeinfo = Station_0020CF3B.objects.filter(date=dates[i])
            if (timeinfo.exists() == False):
                Station_0020CF3B.objects.create(date=dates[i], air_temp_avg=air_temperature_avg[i], relative_humidity_avg=relative_humidity_avg[i], soil_temp_avg=soil_temperature_avg[i], soil_moisture=soil_moisture_avg[i])
                count += 1
    print('[UPDATE] Update for last day on 0020CF3B complete. ' + str(count) + ' rows added.' )


def station_002099C5_update():
    print('[UPDATE] Starting update for last day on 002099C5.')
    apiRoute = '/data/002099C5/hourly/last/3d'
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

    count = 0
    for i in range(1, len(air_t['values']['avg'])):
        if ((air_temp[i] != None) & (rel_hum[i] != None) & (s_t_1[i] != None) & (s_t_2[i] != None)):
            timeinfo = Station_002099C5.objects.filter(date=dates[i])
            if (timeinfo.exists() == False):
                Station_002099C5.objects.create(date=dates[i], air_temp_avg=air_temp[i], relative_humidity_avg=rel_hum[i], soil_temp_1=s_t_1[i], soil_temp_2=s_t_2[i])
                count += 1
    print('[UPDATE] Update for last day on 002099C5 complete. ' + str(count) + ' rows added.' )

def station_00000235_update():
    print('[UPDATE] Starting update for last day on 00000235.')
    apiRoute = '/data/00000235/hourly/last/3d'
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

    count = 0

    for i in range(1, len(air_t['values']['avg'])):
        if ((air_temp[i] != None) & (rel_hum[i] != None) & (dew_p[i] != None) & (wind_avg[i] != None) & (row[i] != None)):
            timeinfo = Station_00000235.objects.filter(date=dates[i])
            if (timeinfo.exists() == False):
                Station_00000235.objects.create(date=dates[i], air_temp_avg=air_temp[i], relative_humidity_avg=rel_hum[i], dew_point=dew_p[i], wind_speed_avg=wind_avg[i], wind_speed_max=row[i])
                count += 1
    print('[UPDATE] Update for last day on 00000235 complete. ' + str(count) + ' rows added.' )

def get_station_info():
    station_00000235_update()
    station_002099C5_update()
    station_0020CF3B_update()


def start():
    # get_station_info()
    # db_backup()
    scheduler_update = BackgroundScheduler()
    scheduler_update.add_job(get_station_info, 'interval', days=1)
    scheduler_update.start()
    
    scheduler_backup = BackgroundScheduler()
    scheduler_backup.add_job(db_backup, 'interval', days=30)
    scheduler_backup.start()
