import pandas as pd
import pmdarima as pm
import pickle

data_temperature = pd.read_csv('data/temperature.csv', names=['San Francisco'], header=0)
data_temperature.dropna(inplace=True)

temperatures_model = pm.auto_arima(
    data_temperature,
    start_p=1,
    start_q=1,
    test='adf',
    max_p=3,
    max_q=3,
    m=1,
    d=None,
    seasonal=False,
    start_P=0, 
    D=0, 
    trace=True,
    error_action='ignore',  
    suppress_warnings=True, 
    stepwise=True
)

with open('models/temperature.pkl', 'wb') as pkl:
    pickle.dump(temperatures_model, pkl)

data_humidity = pd.read_csv('data/humidity.csv', names=['San Francisco'], header=0)
data_humidity.dropna(inplace=True)

humidity_model = pm.auto_arima(
    data_humidity,
    start_p=1,
    start_q=1,
    test='adf',
    max_p=3,
    max_q=3,
    m=1,
    d=None,
    seasonal=False,
    start_P=0, 
    D=0, 
    trace=True,
    error_action='ignore',  
    suppress_warnings=True, 
    stepwise=True
)

with open('models/humidity.pkl', 'wb') as pkl:
    pickle.dump(humidity_model, pkl)
