from django.shortcuts import render
from pip import main
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.http import JsonResponse
import os
from ml_script import ml_predict_test, ml_predict
import json

def index(request):
    if (request.is_ajax()):
        station_name = 'Station_'
        station_name += request.GET.get('selected_station')
        station_mode = request.GET.get('selected_mode')
        first_date = request.GET.get('first_date')
        first_date += ' 00:00:00'
        second_date = request.GET.get('second_date')
        second_date += ' 23:00:00'
        if (station_name == 'Station_0020CF3B'):
            if (station_mode == 'hourly'):
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date)
            elif (station_mode == 'daily'):
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00")
            elif (station_mode == 'weekly'):                
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00")
                station_dates = selected.values_list('date')[::7]
                station_temp = selected.values_list('air_temp_avg')[::7]
                station_soil_temp = selected.values_list('soil_temp_avg')[::7]
                station_humidity = selected.values_list('relative_humidity_avg')[::7]
                station_soil_moisture = selected.values_list('soil_moisture')[::7]
                return JsonResponse({
                                    'name': station_name,
                                    'mode': station_mode, 
                                    'dates' : list(station_dates),
                                    'air_temp_avg' : list(station_temp), 
                                    'soil_temp_avg' : list(station_soil_temp),
                                    'relative_humidity_avg' : list(station_humidity),
                                    'soil_moisture' : list(station_soil_moisture)
                                }, status=200)
            # 0020CF3B stats : air_temp_avg, date, id, relative_humidity_avg, soil_moisture, soil_temp_avg
            station_dates = selected.values_list('date')
            station_temp = selected.values_list('air_temp_avg')
            station_soil_temp = selected.values_list('soil_temp_avg')           
            station_humidity = selected.values_list('relative_humidity_avg')
            station_soil_moisture = selected.values_list('soil_moisture')
            return JsonResponse({
                                    'name': station_name,
                                    'mode': station_mode, 
                                    'dates' : list(station_dates),
                                    'air_temp_avg' : list(station_temp), 
                                    'soil_temp_avg' : list(station_soil_temp),
                                    'relative_humidity_avg' : list(station_humidity),
                                    'soil_moisture' : list(station_soil_moisture)
                                }, status=200)
        if (station_name == 'Station_002099C5'):
            if (station_mode == 'hourly'):
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date)
            elif (station_mode == 'daily'):
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00")
            elif (station_mode == 'weekly'):                
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00")
                station_dates = selected.values_list('date')[::7]
                station_temp = selected.values_list('air_temp_avg')[::7]
                station_humidity = selected.values_list('relative_humidity_avg')[::7]
                station_soil_temp_1 = selected.values_list('soil_temp_1')[::7]
                station_soil_temp_2 = selected.values_list('soil_temp_2')[::7]
                station_soil_temp_3 = selected.values_list('soil_temp_3')[::7]
                main_station_data = Station_0020CF3B.objects.all()
                data_temp = main_station_data.values_list('air_temp_avg', flat=True)
                data_humidity = main_station_data.values_list('relative_humidity_avg', flat=True)
                data_soil_temp = main_station_data.values_list('soil_temp_avg', flat=True)
                data_moist = main_station_data.values_list('soil_moisture', flat=True)
                main_station_data2 = Station_002099C5.objects.all()
                data2_temp = main_station_data2.values_list('air_temp_avg', flat=True)
                data2_humidity = main_station_data2.values_list('relative_humidity_avg', flat=True)
                data2_soil_temp = main_station_data2.values_list('soil_temp_1', flat=True)
                predict = ml_predict_test({
                    'Air Temperature' : list(data_temp), 
                    'Relative Humidity' : list(data_humidity), 
                    'Soil Temperature' : list(data_soil_temp),
                    'Soil Moisture' : list(data_moist)
                },
                {
                    'Air Temperature' : list(data2_temp), 
                    'Relative Humidity' : list(data2_humidity), 
                    'Soil Temperature' : list(data2_soil_temp)
                })
                file_dir = '../../data2.csv'
                # predict = ml_predict_test(file_dir)[::7]
                return JsonResponse({
                                    'name': station_name,
                                    'dates' : list(station_dates), 
                                    'air_temp_avg' : list(station_temp), 
                                    'relative_humidity_avg' : list(station_humidity), 
                                    'soil_temp_1' : list(station_soil_temp_1),
                                    'soil_temp_2' : list(station_soil_temp_2),
                                    'soil_temp_3' : list(station_soil_temp_3),
                                    'predict' : predict
                                    }, status=200)
            # 002099C5 stats : air_temp_avg, date, id, relative_humidity_avg, soil_temp_1, soil_temp_2, soil_temp_3
            station_dates = selected.values_list('date')
            station_temp = selected.values_list('air_temp_avg')
            station_humidity = selected.values_list('relative_humidity_avg')
            station_soil_temp_1 = selected.values_list('soil_temp_1')
            station_soil_temp_2 = selected.values_list('soil_temp_2')
            station_soil_temp_3 = selected.values_list('soil_temp_3')
            main_station_data = Station_0020CF3B.objects.all()
            data_temp = main_station_data.values_list('air_temp_avg', flat=True)
            data_humidity = main_station_data.values_list('relative_humidity_avg', flat=True)
            data_soil_temp = main_station_data.values_list('soil_temp_avg', flat=True)
            data_moist = main_station_data.values_list('soil_moisture', flat=True)
            main_station_data2 = Station_002099C5.objects.all()
            data2_temp = main_station_data2.values_list('air_temp_avg', flat=True)
            data2_humidity = main_station_data2.values_list('relative_humidity_avg', flat=True)
            data2_soil_temp = main_station_data2.values_list('soil_temp_1', flat=True)
            predict = ml_predict_test(
                {
                    'Air Temperature' : list(data_temp), 
                    'Relative Humidity' : list(data_humidity), 
                    'Soil Temperature' : list(data_soil_temp),
                    'Soil Moisture' : list(data_moist)
                },
                {
                    'Air Temperature' : list(data2_temp), 
                    'Relative Humidity' : list(data2_humidity), 
                    'Soil Temperature' : list(data2_soil_temp)
                })
            # file_dir = '../../data2.csv'
            # predict = ml_predict(file_dir)

            return JsonResponse({
                                    'name': station_name,
                                    'dates' : list(station_dates), 
                                    'air_temp_avg' : list(station_temp), 
                                    'relative_humidity_avg' : list(station_humidity), 
                                    'soil_temp_1' : list(station_soil_temp_1),
                                    'soil_temp_2' : list(station_soil_temp_2),
                                    'soil_temp_3' : list(station_soil_temp_3),
                                    'predict' : predict
                                }, status=200)
        if (station_name == 'Station_00000235'):
            if (station_mode == 'hourly'):
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date)
            elif (station_mode == 'daily'):
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00")
            elif (station_mode == 'weekly'):                
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00")
                station_dates = selected.values_list('date')[::7]
                station_temp = selected.values_list('air_temp_avg')[::7]
                station_dew_point = selected.values_list('dew_point')[::7]
                station_humidity = selected.values_list('relative_humidity_avg')[::7]
                station_wind_speed_avg = selected.values_list('wind_speed_avg')[::7]
                station_wind_speed_max = selected.values_list('wind_speed_max')[::7]
                return JsonResponse({
                                    'name': station_name,
                                    'mode': station_mode, 
                                    'dates' : list(station_dates),
                                    'air_temp_avg' : list(station_temp), 
                                    'dew_point' : list(station_dew_point),
                                    'relative_humidity_avg' : list(station_humidity),
                                    'wind_speed_avg' : list(station_wind_speed_avg),
                                    'wind_speed_max' : list(station_wind_speed_max),
                                }, status=200)
            # 00000235: id, date, air_temp_avg, relative_humidity_avg, dew_point, wind_speed_avg, wind_speed_max
            station_dates = selected.values_list('date')
            station_temp = selected.values_list('air_temp_avg')
            station_humidity = selected.values_list('relative_humidity_avg')
            station_dew_point = selected.values_list('dew_point')
            station_wind_speed_avg = selected.values_list('wind_speed_avg')
            station_wind_speed_max = selected.values_list('wind_speed_max')
            return JsonResponse({
                                    'name': station_name,
                                    'mode': station_mode, 
                                    'dates' : list(station_dates),
                                    'air_temp_avg' : list(station_temp), 
                                    'relative_humidity_avg' : list(station_humidity),
                                    'dew_point' : list(station_dew_point),
                                    'wind_speed_avg' : list(station_wind_speed_avg),
                                    'wind_speed_max' : list(station_wind_speed_max),
                                }, status=200)
        
    return render(request, "polls/header.html")
    

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out succesfully")
    return redirect("/login")

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request,
                    template_name="polls/login.html",
                    context={"form": form})