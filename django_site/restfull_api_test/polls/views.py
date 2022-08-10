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
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import datetime
import math
from plotly.offline import plot
from django.db.models import F

#функция создания графиков
def graph_make(data, data_name):
    #получает данные из базы данных, загружает в датафрейм и транспонирует, назначает названия столбцов
    df = pd.DataFrame(data = data)
    datafr = df.transpose()
    datafr.columns = data_name
    #удаляет даты из датафрейма и загружает в отдельную переменную
    date_time = pd.to_datetime(datafr.pop(datafr.columns[0]), format='%Y-%m-%d %H:%M:%S')
    plot_cols = data_name[1:]
    plot_features = datafr[plot_cols]
    #алгоритм задания грида графиков
    #если количество переменных является квадратом целого числа - количество строк и столбцов грида равняется этому числу
    if (math.sqrt(len(plot_cols)).is_integer()):
        row = int(math.sqrt(len(plot_cols)))
        col = int(math.sqrt(len(plot_cols)))
    #иначе количество строк равняется квадратному корню из количества переменных, округленному в большую сторону
    else:
        row = int(math.ceil(math.sqrt(len(plot_cols))))
        #а количество столбцов округляется к ближайшему целому числу
        if(math.sqrt(len(plot_cols)) < math.trunc(math.sqrt(len(plot_cols))) + 0.5):
            col = int(math.floor(math.sqrt(len(plot_cols))))
        else:
            col = int(math.ceil(math.sqrt(len(plot_cols))))
    #задание количества графиков
    #в дальнейшем, если количество графиков не соответствует объему грида - графики в нижней строке грида будут масштабироваться
    #но пока он просто рисует графики по гриду, а пустые ячейки грида оставляет пустыми. Потом поправлю
    if (len(plot_cols)%2==0):
        fig = make_subplots(rows=row, cols=col, subplot_titles=(plot_cols), shared_xaxes=False)
    else:
        # specs = []
        # for i in range(1, len(plot_cols), 1):
        #     specs += [[{}, {}, {}]]
        # specs += [[{"colspan": row}, None,{}]]
        # specs += [[{}, {}, {}]]
        fig = make_subplots(rows=row, cols=col, subplot_titles=(plot_cols), shared_xaxes=False)
    #отрисовка графиков
    #просто вложенный цикл проходит по всем ячейкам грида и отрисовывает графики в каждой (пока количество ячеек не превысит количество переменных)
    num_name = 1
    for row_num in range(1, row, 1):
        for col_num in range(1, col, 1):
            if(row_num * col_num <= len(plot_cols)):
                fig.add_trace(go.Scatter(x=date_time, y=plot_features[str(plot_cols[num_name - 1])], name = plot_cols[num_name - 1]), row = row_num, col= col_num)
                fig.update_xaxes(title_text="Date", row=row_num, col=col_num)
                fig.update_yaxes(title_text=str(plot_cols[num_name - 1]), row=row_num, col=col_num)
                num_name += 1
    #Добавляет название и меняет высоту подложки 
    fig.update_layout(title_text="Meteo Data", height=700)
    #Возвращает код для отрисовки графиков
    fig_plot = plot(fig, output_type='div', include_plotlyjs=True)
    return fig_plot

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
                selected = eval(station_name).objects.annotate(idmod7=F('id') % 7).filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00", idmod7=0)
            # 0020CF3B stats : air_temp_avg, date, id, relative_humidity_avg, soil_moisture, soil_temp_avg
            station_dates = selected.values_list('date', flat = True)
            station_temp = selected.values_list('air_temp_avg', flat = True)
            station_soil_temp = selected.values_list('soil_temp_avg', flat = True)           
            station_humidity = selected.values_list('relative_humidity_avg', flat = True)
            station_soil_moisture = selected.values_list('soil_moisture', flat = True)
            data_name_1 = ['date', 'air_temp_avg', 'soil_temp_avg', 'relative_humidity_avg', 'soil_moisture']
            data_1 = [station_dates, station_temp, station_soil_temp, station_humidity, station_soil_moisture]
            print(data_1)
            text_chart = graph_make(data = data_1, data_name = data_name_1)
            return JsonResponse({
                                    'name': station_name,
                                    'mode': station_mode, 
                                    'dates' : list(station_dates),
                                    'air_temp_avg' : list(station_temp), 
                                    'soil_temp_avg' : list(station_soil_temp),
                                    'relative_humidity_avg' : list(station_humidity),
                                    'soil_moisture' : list(station_soil_moisture),
                                    'graph': str(text_chart)
                                }, status=200)
        if (station_name == 'Station_002099C5'):
            if (station_mode == 'hourly'):
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date)
            elif (station_mode == 'daily'):
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00")
            elif (station_mode == 'weekly'):                
                selected = eval(station_name).objects.annotate(idmod7=F('id') % 7).filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00", idmod7=0)
            # 002099C5 stats : air_temp_avg, date, id, relative_humidity_avg, soil_temp_1, soil_temp_2, soil_temp_3
            station_dates = selected.values_list('date', flat = True)
            station_temp = selected.values_list('air_temp_avg', flat = True)
            station_humidity = selected.values_list('relative_humidity_avg', flat = True)
            station_soil_temp_1 = selected.values_list('soil_temp_1', flat = True)
            station_soil_temp_2 = selected.values_list('soil_temp_2', flat = True)
            station_soil_temp_3 = selected.values_list('soil_temp_3', flat = True)
            data_2 = [station_dates, station_temp, station_humidity, station_soil_temp_1, station_soil_temp_2, station_soil_temp_3]
            data_name_2 = ['date', 'air_temp_avg', 'relative_humidity_avg', 'soil_temp_1', 'soil_temp_2', 'soil_temp_3']
            text_chart = graph_make(data = data_2, data_name = data_name_2)
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
                                    'predict' : predict,
                                    'graph': str(text_chart)
                                }, status=200)
        if (station_name == 'Station_00000235'):
            if (station_mode == 'hourly'):
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date)
            elif (station_mode == 'daily'):
                selected = eval(station_name).objects.filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00")
            elif (station_mode == 'weekly'):                
                selected = eval(station_name).objects.annotate(idmod7=F('id') % 7).filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00", idmod7=0)
            # 00000235: id, date, air_temp_avg, relative_humidity_avg, dew_point, wind_speed_avg, wind_speed_max
            station_dates = selected.values_list('date', flat = True)
            station_temp = selected.values_list('air_temp_avg', flat = True)
            station_humidity = selected.values_list('relative_humidity_avg', flat = True)
            station_dew_point = selected.values_list('dew_point', flat = True)
            station_wind_speed_avg = selected.values_list('wind_speed_avg', flat = True)
            station_wind_speed_max = selected.values_list('wind_speed_max', flat = True)
            data_3 = [station_dates, station_temp, station_humidity, station_dew_point, station_wind_speed_avg, station_wind_speed_max]
            data_name_3 = ['date', 'air_temp_avg', 'relative_humidity_avg', 'dew_point', 'wind_speed_avg', 'wind_speed_max']
            text_chart = graph_make(data = data_3, data_name = data_name_3)
            return JsonResponse({
                                    'name': station_name,
                                    'mode': station_mode, 
                                    'dates' : list(station_dates),
                                    'air_temp_avg' : list(station_temp), 
                                    'relative_humidity_avg' : list(station_humidity),
                                    'dew_point' : list(station_dew_point),
                                    'wind_speed_avg' : list(station_wind_speed_avg),
                                    'wind_speed_max' : list(station_wind_speed_max),
                                    'graph': str(text_chart)
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