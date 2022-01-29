from django.shortcuts import render
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.http import JsonResponse
import json

def index(request):
    if (request.is_ajax()):
        station_name = 'Station_'
        station_name += request.GET.get('selected_station')
        if (station_name == 'Station_0020CF3B'):            
            # 0020CF3B stats : air_temp_avg, date, id, relative_humidity_avg, soil_moisture, soil_temp_avg
            station_dates = eval(station_name).objects.all()[:50].values_list('date')
            station_temp = eval(station_name).objects.all()[:50].values_list('air_temp_avg')
            station_soil_temp = eval(station_name).objects.all()[:50].values_list('soil_temp_avg')           
            station_humidity = eval(station_name).objects.all()[:50].values_list('relative_humidity_avg')
            station_soil_moisture = eval(station_name).objects.all()[:50].values_list('soil_moisture')
            return JsonResponse({
                                    'name': station_name, 
                                    'dates' : list(station_dates),
                                    'air_temp_avg' : list(station_temp), 
                                    'soil_temp_avg' : list(station_soil_temp),
                                    'relative_humidity_avg' : list(station_humidity),
                                    'soil_moisture' : list(station_soil_moisture)
                                }, status=200)
        if (station_name == 'Station_002099C5'):
            # 002099C5 stats : air_temp_avg, date, id, relative_humidity_avg, soil_temp_1, soil_temp_2, soil_temp_3
            station_dates = eval(station_name).objects.all()[:50].values_list('date')
            station_temp = eval(station_name).objects.all()[:50].values_list('air_temp_avg')
            station_humidity = eval(station_name).objects.all()[:50].values_list('relative_humidity_avg')
            station_soil_temp_1 = eval(station_name).objects.all()[:50].values_list('soil_temp_1')
            station_soil_temp_2 = eval(station_name).objects.all()[:50].values_list('soil_temp_2')
            station_soil_temp_3 = eval(station_name).objects.all()[:50].values_list('soil_temp_3')
            return JsonResponse({
                                    'name': station_name,
                                    'dates' : list(station_dates), 
                                    'air_temp_avg' : list(station_temp), 
                                    'relative_humidity_avg' : list(station_humidity), 
                                    'soil_temp_1' : list(station_soil_temp_1),
                                    'soil_temp_2' : list(station_soil_temp_2),
                                    'soil_temp_3' : list(station_soil_temp_3),
                                }, 
                                    status=200)
    latest_twenty = Station_0020CF3B.objects.all()[:20]
    return render(request, "polls/header.html", {'data' : latest_twenty})
    

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