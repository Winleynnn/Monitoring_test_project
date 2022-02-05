from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import csv
import json

def ml_predict(x_test):
    #### На этом обучаем
    date1 = datetime.now()    
    print(datetime.now(), ' ml_predict start')
    df_train = pd.read_csv('../../data.csv')
    X = df_train[['Air Temperature', 'Relative Humidity', 'Soil Temperature']]
    y = df_train['Soil Moisture']
    ###Тут из цсвшки забираем нужные данные
    x_test = pd.read_csv(x_test)[['Air Temperature', 'Relative Humidity', 'Soil Temperature']]
    X_train, y_train = X, y
    clf = RandomForestRegressor(
                                criterion='friedman_mse',
                                max_features=1.0,
                                n_estimators=512,
                                n_jobs=-1,
                                random_state=1,
                                warm_start=True
                                )
    clf.fit(X_train, y_train)
    y_pred = clf.predict(x_test)
    # with open('prediction.csv', 'w', newline='') as csv_file:
    #     csv_writer = csv.writer(csv_file)
    #     for item in y_pred:
    #         csv_writer.writerow([item])
    date2 = datetime.now()
    print(datetime.now(), ' ml_predict stop')
    print('total time ', (date2 - date1))
    return(list(y_pred.round(2)))

def ml_predict_test(data, data2):
    date1 = datetime.now()
    print(datetime.now(), ' test start')
    df_train = pd.DataFrame.from_dict(data)
    X = df_train[['Air Temperature', 'Relative Humidity', 'Soil Temperature']]
    y = df_train['Soil Moisture']
    x_test = pd.DataFrame.from_dict(data2)
    X_train, y_train = X, y
    clf = RandomForestRegressor(
                                criterion='friedman_mse',
                                max_features=1.0,
                                n_estimators=512,
                                n_jobs=-1,
                                random_state=1,
                                warm_start=True
                                )
    clf.fit(X_train, y_train)
    y_pred = clf.predict(x_test)
    date2 = datetime.now()
    print(datetime.now(), ' test stop')
    print('total time ', (date2 - date1))
    return(list(y_pred.round(2)))


