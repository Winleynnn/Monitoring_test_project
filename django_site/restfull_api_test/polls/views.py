from django.shortcuts import render
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.http import JsonResponse
import os
from ml_script import ml_predict
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
                                    'soil_moisture' : list(station_soil_moisture),
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
                                    'soil_moisture' : list(station_soil_moisture),
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
                file_dir = '../../data2.csv'
                predict = ml_predict(file_dir)[::7]
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
            file_dir = '../../data2.csv'
            predict = ml_predict(file_dir)
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