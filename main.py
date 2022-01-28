import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from lightgbm import LGBMRegressor
from xgboost.sklearn import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn import metrics
from sklearn.model_selection import GridSearchCV


clt_lst = [
    RandomForestRegressor, #0.674
    # LinearRegression, #0.421
    # # LogisticRegression,
    # LGBMRegressor, #0.629
    # XGBRegressor,#0.635
    # CatBoostRegressor, #0.6739
    # SGDRegressor, #NANI?
    # KernelRidge,#0.372
    # ElasticNet, #0.413
    # BayesianRidge, #0.422
    # GradientBoostingRegressor, #0.614
    # SVR #0.4301
]

df = pd.read_csv('data.csv')
X = df[['Air Temperature', 'Relative Humidity', 'Soil Temperature']]  # Features
y = df['Soil Moisture']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
for clt in clt_lst:
    clf = clt(
        # n_estimators=200,
        n_jobs=-1,
        random_state=42,
        max_depth=10,
        min_samples_leaf=4,
        min_samples_split=8,
        n_estimators=1
    )
    # params = {
    #     'n_estimators': range(1, 10),
    #     # 'max_depth': range(6, 20),
    #     'min_samples_leaf': range(1, 8),
    #      'min_samples_split': range(17, 40),
    #     #'n_estimators': [10, 1, 3, 2],
    #     'max_depth': range(200, 300, 5),
    #     #'min_samples_leaf': [4, 5, 3, 7],
    #     #'min_samples_split': [8, 13, 9, 18, 27, 19, 32]
    # }
    # grid = GridSearchCV(clf, params, cv=5, n_jobs=-1)
    # grid.fit(X, y)
    # print(grid.best_params_)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accur_sc = clf.score(X_test, y_test)
    print(f"Accuracy: {accur_sc}, classifier - {clt}")
    with open('selection_result.txt', 'a') as history_data:
        history_data.write(f"\nAccuracy: {accur_sc}, params: {clf}")

###{'max_depth': 13, 'min_samples_leaf': 4, 'min_samples_split': 8, 'n_estimators': 10} 0.6428638096761063
###{'max_depth': 10, 'min_samples_leaf': 4, 'min_samples_split': 8, 'n_estimators': 1}
###{'max_depth': 9, 'min_samples_leaf': 4, 'min_samples_split': 13, 'n_estimators': 3} 0.5864482472612953
###{'max_depth': 13, 'min_samples_leaf': 5, 'min_samples_split': 9, 'n_estimators': 3} 0.5907086223683005
###{'max_depth': 7, 'min_samples_leaf': 4, 'min_samples_split': 18, 'n_estimators': 2} 0.5717653494775098
###{'max_depth': 16, 'min_samples_leaf': 5, 'min_samples_split': 27, 'n_estimators': 2} 0.5953679271698983
###{'max_depth': 17, 'min_samples_leaf': 3, 'min_samples_split': 19, 'n_estimators': 1} 0.5046638840740791
###{'max_depth': 19, 'min_samples_leaf': 7, 'min_samples_split': 32, 'n_estimators': 1} 0.5055849495642504
###Total {'max_depth': 17, 'min_samples_leaf': 5, 'min_samples_split': 18, 'n_estimators': 2} 0.5479306633854197
###{'max_depth': 240, 'min_samples_leaf': 3, 'min_samples_split': 27, 'n_estimators': 1} 0.5429858295355905
###{'max_depth': 260, 'min_samples_leaf': 3, 'min_samples_split': 8, 'n_estimators': 2} 0.5698770200885916
###{'max_depth': 225, 'min_samples_leaf': 1, 'min_samples_split': 29, 'n_estimators': 1} 0.4395212596655207