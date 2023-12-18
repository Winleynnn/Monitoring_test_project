from django.shortcuts import render
from pip import main
from .models import *
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
import os
from ml_script import ml_predict_test, ml_predict
import json
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import math
from plotly.offline import plot
from django.apps import AppConfig, apps
# from AppConfig import get_model
from django.utils.module_loading import import_string
from django.db.models import F, Min, Max
from django.http import Http404
from django.db.models.functions import Greatest, Least

#функция обработки данных
def pre_data(data, data_name):
    #получает данные из базы данных, загружает в датафрейм и транспонирует, назначает названия столбцов
    df = pd.DataFrame(data = data)
    datafr = df.transpose()
    datafr.columns = list(data_name.keys())
    #удаляет даты из датафрейма и загружает в отдельную переменную
    date_time = pd.to_datetime(datafr.pop(datafr.columns[0]), format='%Y-%m-%d %H:%M:%S')
    plot_cols = list(data_name.keys())[1:]
    col_names = list(data_name.values())[1:]
    plot_features = datafr[plot_cols]
    return date_time, plot_cols, col_names, plot_features

#функция сбора описательной статистики
def data_stat(col_names, plot_features):
    df = plot_features.copy()
    df.columns = col_names
    df = df.apply(pd.to_numeric)
    df_stat = pd.DataFrame(df.describe())
    df_info = pd.DataFrame(df.info())
    return df_stat.to_html(), df_info.to_html()

#функция создания графика тепловой карты корреляции между переменными
def graph_corr(col_names, plot_features):
    df = plot_features.copy()
    df.columns = col_names
    df = df.apply(pd.to_numeric)
    fig = px.imshow(df.corr(),
                labels=dict(x="Variables", y="Variables", color="Correlation Coefficient"),
                color_continuous_scale=px.colors.sequential.Agsunset, text_auto = True
               )
    fig.update_xaxes(side="top")
    fig.update_layout(title_text="Тепловая карта коэффициента корреляции")
    corr_plot = plot(fig, output_type='div', include_plotlyjs=True)
    return corr_plot

#функция создания графика диаграммы размаха
def graph_box(col_names, plot_features, plot_cols):
    if (math.sqrt(len(plot_cols)).is_integer()):
        row = int(math.sqrt(len(plot_cols)))
        col = int(math.sqrt(len(plot_cols)))
    else:
        row = int(math.ceil(math.sqrt(len(plot_cols))))
        #а количество столбцов округляется к ближайшему целому числу
        if(math.sqrt(len(plot_cols)) < math.trunc(math.sqrt(len(plot_cols))) + 0.5):
            col = int(math.floor(math.sqrt(len(plot_cols))))
        else:
            col = int(math.ceil(math.sqrt(len(plot_cols))))
    if (len(plot_cols)%2==0):
        fig = make_subplots(rows=row, cols=col, subplot_titles=(col_names), shared_xaxes=False)
    else:
        fig = make_subplots(rows=row, cols=col, subplot_titles=(col_names), shared_xaxes=False)
    num_name = 1
    for row_num in range(1, row+1, 1):
        for col_num in range(1, col+1, 1):
            if(row_num * col_num <= len(plot_cols) and num_name-1 < len(plot_cols)):
                #print(plot_cols[num_name - 1])
                #print(plot_features)
                fig.add_trace(go.Box(y=plot_features[str(plot_cols[num_name - 1])], 
                    name = col_names[num_name - 1]), row = row_num, col= col_num)
                fig.update_yaxes(title_text=str(col_names[num_name - 1]), row=row_num, col=col_num)
                num_name += 1
    #Добавляет название и меняет высоту подложки 
    fig.update_layout(title_text="Диаграммы размаха переменных")
    #Возвращает код для отрисовки графиков
    fig_plot = plot(fig, output_type='div', include_plotlyjs=True)
    return fig_plot

#функция создания графиков динамики временного ряда
def graph_make(date_time, plot_cols, col_names, plot_features):
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
        fig = make_subplots(rows=row, cols=col, subplot_titles=(col_names), shared_xaxes=False)
    else:
        # specs = []
        # for i in range(1, len(plot_cols), 1):
        #     specs += [[{}, {}, {}]]
        # specs += [[{"colspan": row}, None,{}]]
        # specs += [[{}, {}, {}]]
        fig = make_subplots(rows=row, cols=col, subplot_titles=(col_names), shared_xaxes=False)
    #отрисовка графиков
    #просто вложенный цикл проходит по всем ячейкам грида и отрисовывает графики в каждой (пока количество ячеек не превысит количество переменных)
    num_name = 1
    for row_num in range(1, row+1, 1):
        for col_num in range(1, col+1, 1):
            if(row_num * col_num <= len(plot_cols) and num_name-1 < len(plot_cols)):
                print(row_num * col_num <= len(plot_cols))
                print((num_name-1) < len(plot_cols))    
                print(row_num*col_num)
                print(len(plot_cols))
                print("num_name " + str(num_name))
                fig.add_trace(go.Scatter(x=date_time, y=plot_features[str(plot_cols[num_name - 1])], 
                    name = col_names[num_name - 1]), row = row_num, col= col_num)
                fig.update_xaxes(title_text="Дата", row=row_num, col=col_num)
                fig.update_yaxes(title_text=str(col_names[num_name - 1]), row=row_num, col=col_num)
                num_name += 1
    #Добавляет название и меняет высоту подложки 
    fig.update_layout(title_text="Динамика изменения метеорологических параметров")
    #Возвращает код для отрисовки графиков
    fig_plot = plot(fig, output_type='div', include_plotlyjs=True)
    return fig_plot

def index(request):
    if (request.is_ajax()):
        if request.user.is_authenticated:
                username = request.user.username
                ret = User_Models.objects.filter(login=username)
                if ret:
                    stations = ret.values_list('station_info', flat = True)
                    temp_keys = ""
                    for key in stations[0].keys():
                        temp_keys += key + " "
                    temp_keys = temp_keys.strip(" ")
                    stations = temp_keys.split(' ')
        else:
            logout_request(request)
            redirect('/login')
        print('action ' + str(request.GET.get('action')))
        if (request.GET.get('action') == 'take_info'):
            print("take_info")
            temp = request.GET.get('selected_station')
            if (temp in stations):
                print("temp + {0}", temp)
                print(stations)
                station_name = 'Station_'
                station_name += request.GET.get('selected_station')
                station_mode = request.GET.get('selected_mode')
                first_date = request.GET.get('first_date')
                first_date += ' 00:00:00'
                second_date = request.GET.get('second_date')
                second_date += ' 23:00:00'
                print('---------------------GO RESPONSE---------------------')
                name = station_name
                mode = station_mode
                date1 = first_date
                date2 = second_date
                columns = list(apps.get_model(app_label="polls",model_name = station_name)._meta.get_fields(include_parents=False))
                columns.pop(0)
                # print(columns)
                column_names = list()
                column_aliases = list()
                for f in columns:
                    column_names.append(f.name)
                    column_aliases.append(f.verbose_name)
                if (station_mode == 'hourly'):
                    selected = apps.get_model(app_label="polls",model_name = station_name).objects.filter(date__gte=first_date, date__lte=second_date)
                elif (station_mode == 'daily'):
                    selected = apps.get_model(app_label="polls",model_name = station_name).objects.filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00")
                elif (station_mode == 'weekly'):                
                    selected = apps.get_model(app_label="polls",model_name = station_name).objects.annotate(idmod7=F('id') % 7).filter(date__gte=first_date, date__lte=second_date, date__icontains="00:00:00", idmod7=0)
                info = {}
                data_name_1 = {}
                data_1 = []
                info['names'] = column_names
                # print(column_names)
                # print(info['names'])
                info['aliases'] = column_aliases
                for column in column_names:
                    # print(list(selected.values_list(column, flat=True)))
                    info[column] = list(selected.values_list(column, flat=True))
                    # print(column)
                    # print(info[column])
                for i in range(0, len(column_names)):
                    data_name_1[column_names[i]] = column_aliases[i]
                    data_1.append(info[column_names[i]])
                # data_name_1 = {'date':'Дата', 'air_temp_avg':'Средняя температура воздуха', 'soil_temp_avg':'Средняя температура почвы', 'relative_humidity_avg':'Относительная влажность воздуха', 'soil_moisture':'Влажность почвы'}
                # data_1 = [station_dates, station_temp, station_soil_temp, station_humidity, station_soil_moisture]
                #print(data_1)
                # text_chart = graph_make(data = data_1, data_name = data_name_1)
                date_time_1, plot_cols_1, col_names_1, plot_features_1 = pre_data(data = data_1, data_name = data_name_1)
                text_chart = graph_make(date_time = date_time_1, plot_cols = plot_cols_1, col_names = col_names_1, plot_features = plot_features_1)
                stat, inform = data_stat(col_names = col_names_1, plot_features = plot_features_1)
                #print(plot_features_1)
                corr_chart = graph_corr(col_names = col_names_1, plot_features = plot_features_1)
                box_chart = graph_box(col_names = col_names_1, plot_features = plot_features_1, plot_cols = plot_cols_1)
                info['graph'] = str(text_chart)
                info['statistics'] = str(stat)
                info['information'] = str(inform)
                info['correlation_chart'] = str(corr_chart)
                info['box_plot_chart'] = str(box_chart)
                info['name'] = name
                username = request.user.username
                ret = User_Models.objects.filter(login=username)
                if ret:
                    stations = ret.values_list('station_info', flat = True)
                    print(stations)
                    # print(stations[0].keys())
                    # for key in stations[0].keys():
                    #     print(key)
                    #     print(stations[0][key])
                    #     if 'download' in stations[0][key]:
                    #         print(str(key) + ' True')
                    temp_keys = ""
                    temp_rights = list()
                    for key in stations[0].keys():
                        temp_keys += key + " "
                        temp_rights.append(stations[0][key])
                    print(temp_rights)
                    temp_keys = temp_keys.strip(' ')
                    print(temp_keys)
                    stations = temp_keys.split(' ')
                    info['stations'] = stations
                    info['rights'] = temp_rights
                return JsonResponse(info, status=200)
            else:
                logout_request(request)
                redirect("/login")
        elif (request.GET.get('action') == 'get_stations'):
            print('get_stations')
            if request.user.is_authenticated:
                username = request.user.username
                ret = User_Models.objects.filter(login=username)
                if ret:
                    stations = ret.values_list('station_info', flat = True)
                    print(stations)
                    # print(stations[0].keys())
                    # for key in stations[0].keys():
                    #     print(key)
                    #     print(stations[0][key])
                    #     if 'download' in stations[0][key]:
                    #         print(str(key) + ' True')
                    temp_keys = ""
                    temp_rights = list()
                    for key in stations[0].keys():
                        temp_keys += key + " "
                        temp_rights.append(stations[0][key])
                    print(temp_rights)
                    temp_keys = temp_keys.strip(' ')
                    stations = temp_keys.split(' ')
                    return JsonResponse({
                        'stations': list(stations),
                        'rights': list(temp_rights)
                    })
                else:
                    return render(request, 'polls/404.html')
        elif (request.GET.get('action') == 'get_station_dates'):
            print('get_stat_dates')
            station_name = 'Station_'
            station_name += request.GET.get('station')
            max_time = apps.get_model(app_label='polls', model_name=station_name).objects.aggregate(Max('date'))
            min_time = apps.get_model(app_label='polls', model_name=station_name).objects.aggregate(Min('date'))
            min_time = min_time['date__min'].split(' ')[0]
            max_time = max_time['date__max'].split(' ')[0]
            return JsonResponse({
                'min_time': min_time,
                'max_time': max_time
            })
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

def feedback(request):
    return render(request, 'polls/feedbackform.html')

from .forms import NewUserForm

def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = NewUserForm()
    return render(request, 'polls/register.html', {'form': form})

def station_admin(request):
    if request.user.is_superuser:
        if (request.is_ajax()):
            if (request.GET.get('action') == 'load_info'):
                User = get_user_model()
                models = apps.get_app_config('polls').get_models()

                users = User.objects.all()
                user_list = list()
                for user in users:
                    user_list.append(user.username)

                model_list = list()
                for model in models:
                    if "Station_" in str(model.__name__):
                        model_list.append(model.__name__.replace("Station_", ""))
                
                temp_users = dict()
                temp_users['usernames'] = user_list
                temp_users['stations'] = model_list
                
                return JsonResponse(temp_users, status=200)
            elif (request.GET.get('action') == 'get_user_stations'):
                user = request.GET.get('username')
                user_info = User_Models.objects.filter(login=user)
                if user_info:
                    stations = user_info.values_list('station_info', flat = True)
                    temp_keys = ""
                    temp_rights = list()
                    for key in stations[0].keys():
                        temp_keys += key + " "
                        temp_rights.append(stations[0][key])
                    temp_keys = temp_keys.strip(' ')
                    stations = temp_keys.split(' ')
                    return JsonResponse({
                        'stations': list(stations),
                        'rights': list(temp_rights)
                    })
                else:
                    return JsonResponse({
                        'stations': list(),
                        'rights': list()
                    })
        return render(request, 'polls/station_admin.html')
    else: raise Http404
    
def station_admin_add(request):
    if request.user.is_superuser:
        if (request.method == 'POST'):
        # elif (request.GET.get('action') == 'upload'):
            # data = dict(json.loads(request.body))
            # print(data)
            # print(data.keys())
            login = json.loads(request.body)['username']
            data = json.loads(request.body)['stations']
            if bool(data):
                temp = dict()
                for key in data.keys():
                    temp[key] = data[key]
                try:
                    mod = User_Models.objects.get(login=login)
                    mod.delete()
                except:
                    mod = None
                mod = User_Models.objects.create(login=login, station_info=temp)
                mod.save()
            # print(json.loads(request.body))
            # temp = User_Models.objects.create(login='sss', station_info='{"bebra":["gaming"]}')
            # temp.save()
            # User_Models.objects.create(login = data['stations']['username'], station_info = data['stations'])
        json_obj = json.dumps({ "time": '00:00:00', "method": "post" })
        result = HttpResponse(json_obj, 'text/plain', charset='utf-8')
        return result
                # us(rname = json.loads(request.POST.get('stations'))
                # username = username['username']
                # stat_info = json.loads(request.POST.get('stations'))
                # print(username)
                # return JsonResponse({'username':list(username)}, status=200, safe=False)
    else: raise Http404
def not_found(request):
    return render(request, 'polls/404.html')