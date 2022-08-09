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

#ЭТА ФУНКЦИЯ ПРОСТО УЖАСНАЯ И ТРЕБУЕТ СЕРЬЕЗНОЙ ДОРАБОТКИ
def graph_make(data, data_name):
    #dt = pd.read_csv('C:/Users/ralf3/OneDrive/Рабочий стол/Project/django_site/restfull_api_test/Hourly Weather Data in Gallipoli (2008-2021).csv', sep = ';')
    df = pd.DataFrame(data = data)
    datafr = df.transpose()
    print(datafr)
    datafr.columns = data_name
    date_time = pd.to_datetime(datafr.pop(datafr.columns[0]), format='%Y-%m-%d %H:%M:%S')
    plot_cols = data_name[1:]
    # for col in list(datafr.columns.values.tolist()):
    #     plot_cols += col
    #     print(plot_cols)
    plot_features = datafr[plot_cols]
    print(datafr)
    # for i in range(1, len(plot_cols), 1):
    if (math.sqrt(len(plot_cols)).is_integer()):
        row = int(math.sqrt(len(plot_cols)))
        col = int(math.sqrt(len(plot_cols)))
    else:
        row = int(math.ceil(math.sqrt(len(plot_cols))))
        if(math.sqrt(len(plot_cols)) < math.trunc(math.sqrt(len(plot_cols))) + 0.5):
            col = int(math.floor(math.sqrt(len(plot_cols))))
        else:
            col = int(math.ceil(math.sqrt(len(plot_cols))))
    if (len(plot_cols)%2==0):
        fig = make_subplots(rows=row, cols=col, subplot_titles=(plot_cols), shared_xaxes=False)
    else:
        fig = make_subplots(rows=row, cols=col, subplot_titles=(plot_cols), shared_xaxes=False)
        # specs=[[{}, {}],
        #    [{"colspan": row}, None]]
    print(row + col)
    num_name = 1
    for p in range(0, row, 1):
        for v in range(0, col, 1):
            row_num = p + 1
            col_num = v + 1
            fig.add_trace(go.Scatter(x=date_time, y=plot_features[str(plot_cols[num_name - 1])], name = plot_cols[num_name - 1]), row = row_num, col= col_num)
            fig.update_xaxes(title_text="Date", row=row_num, col=col_num)
            fig.update_yaxes(title_text=str(plot_cols[num_name - 1]), row=row_num, col=col_num)
            print(plot_features.iloc[:, num_name-1:num_name])
            num_name += 1
        # if(i%2== 0):
        #     fig.add_trace(go.Scatter(x=date_time, y=plot_features.iloc[:, i-1:i], name = plot_cols[i]), row=row -(row - i) + 1, col= col - (col - i) + 1)
        # else:
        #     fig.add_trace(go.Scatter(x=date_time, y=plot_features.iloc[:, i - 1 if (i!=0) else 0:i], name = plot_cols[i]), row=row -(row - i), col= col -(col - i) + 1)
        fig.print_grid()
        print(num_name)
    #dt = plot_features.iloc[:, 0:1]
    #fig.add_trace(go.Scatter(x=date_time, y=dt['air_temp_avg'], name = 'Температура воздуха'), row=1, col=1)
    #print(dt)
    # fig.add_trace(go.Scatter(x=date_time, y=plot_features['soil_temp_avg'], name = 'Температура почвы'), row=1, col=2)
    # fig.add_trace(go.Scatter(x=date_time, y=plot_features['relative_humidity_avg'], name = 'Относительная влажность воздуха'), row=2, col=1)
    # fig.add_trace(go.Scatter(x=date_time, y=plot_features['soil_moisture'], name = 'Влажность почвы'), row=2, col=2)
    # fig.update_xaxes(title_text="Date", row=1, col=1)
    # fig.update_xaxes(title_text="Date", row=1, col=2)
    # fig.update_xaxes(title_text="Date",  row=2, col=1)
    # fig.update_xaxes(title_text="Date", row=2, col=2)
    # fig.update_yaxes(title_text="Temperature", row=1, col=1)
    # fig.update_yaxes(title_text="Soil Temperature", row=1, col=2)
    # fig.update_yaxes(title_text="Air Humidity",  row=2, col=1)
    # fig.update_yaxes(title_text="Soil Moisture", row=2, col=2)
    #for i in range(0, len(plot_cols), 1):
        #временный костыль для работы с одним графиком
        # print(len(plot_cols))
        # if len(plot_cols) == 4:
            # fig.add_trace(
            #     go.Scatter(x=date_time, y=plot_features[plot_cols[i]], name = plot_cols[i]),
            #     row=i+1, col=i+1
            #     )
            # fig.add_trace(go.Scatter(x=date_time, y=plot_features['air_temp_avg']), row=1, col=1)
            # fig.add_trace(go.Scatter(x=date_time, y=plot_features['soil_temp_avg']), row=1, col=2)
            # fig.add_trace(go.Scatter(x=date_time, y=plot_features['relative_humidity_avg']), row=2, col=1)
            # fig.add_trace(go.Scatter(x=date_time, y=plot_features['soil_moisture']), row=2, col=2)
            # fig.update_xaxes(title_text="Date", row=1, col=1)
            # fig.update_xaxes(title_text="Date", row=1, col=2)
            # fig.update_xaxes(title_text="Date",  row=2, col=1)
            # fig.update_xaxes(title_text="Date", row=2, col=2)
            # fig.update_yaxes(title_text="Temperature", row=1, col=1)
            # fig.update_yaxes(title_text="Soil Temperature", row=1, col=2)
            # fig.update_yaxes(title_text="Air Humidity",  row=2, col=1)
            # fig.update_yaxes(title_text="Soil Moisture", row=2, col=2)
            # fig.update_xaxes(title_text="Date", row=i+1, col=i+1)
            # fig.update_yaxes(title_text=plot_cols[i], row=i+1, col=i+1)
        # else:
        #     fig.add_trace(
        #         go.Scatter(x=date_time, y=plot_features[plot_cols[i]], name = plot_cols[i]),
        #         row=i+1, col=i
        #     )
        #     fig.update_xaxes(title_text="Date", row=i+1, col=i)
        #     fig.update_yaxes(title_text=plot_cols[i], row=i+1, col=i)
    
    # Update title and height
    fig.update_layout(title_text="Meteo Data", height=700)
    chart = str(fig.to_html())
    #поменять на относительный путь
    #path_str = "D:/Project/django_site/restfull_api_test/polls/templates/polls/graphs/chart.html"
    path_str = "polls/templates/polls/graphs/chart.html"
    open(path_str, 'w')
    fig.write_html(path_str)
    #return chart
    # context = {'chart': chart}
    # print(chart)
    # return render(request, 'polls/graphs/chart.html', context)]
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
            print(station_dates)
            print(data_1)
            text_chart = graph_make(data = data_1, data_name = data_name_1)
            #df = pd.DataFrame(data = data)
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
            print(station_dates)
            data_2 = [station_dates, station_temp, station_humidity, station_soil_temp_1, station_soil_temp_2, station_soil_temp_3]
            print(data_2)
            data_name_2 = ['date', 'air_temp_avg', 'relative_humidity_avg', 'soil_temp_1', 'soil_temp_2', 'soil_temp_3']
            text_chart = graph_make(data = data_2, data_name = data_name_2)
            #df = pd.DataFrame(data = data)
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
            print(station_dates)
            data_3 = [station_dates, station_temp, station_humidity, station_dew_point, station_wind_speed_avg, station_wind_speed_max]
            print(data_3)
            data_name_3 = ['date', 'air_temp_avg', 'relative_humidity_avg', 'dew_point', 'wind_speed_avg', 'wind_speed_max']
            text_chart = graph_make(data = data_3, data_name = data_name_3)
            #graph_make(data)
            #df = pd.DataFrame(data = data)
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