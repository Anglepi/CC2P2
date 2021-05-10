from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import pmdarima as pm
from datetime import date, datetime, timedelta
import pickle

class ArimaPredictor:

  def loadModel(self):
    with open('models/temperature.pkl', 'rb') as modelFile:
      self.modelTemp = pickle.load(modelFile)

    with open('models/humidity.pkl', 'rb') as modelFile:
      self.modelHum = pickle.load(modelFile)

  def predict(self, hoursPredict):
    startDate = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    arr_hours = pd.date_range(start=startDate, end=(startDate+timedelta(hours=hoursPredict)), freq='H')

    predictTemp = self.modelTemp.predict(n_periods = hoursPredict)
    predictHum = self.modelHum.predict(n_periods = hoursPredict)

    predictions = []
    for hour, temp, hum in zip(arr_hours, predictTemp, predictHum):
      predictions.append({'temp': temp, 'hum': hum, 'hour': hour})

    return {
      'periods': hoursPredict,
      'prediction': predictions
    }