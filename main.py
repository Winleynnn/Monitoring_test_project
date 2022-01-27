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
        n_estimators=69,
        n_jobs=-1,
        random_state=42

    )
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    print(f"Accuracy: {clf.score(X_test, y_test)}, classifier - {clt}")

