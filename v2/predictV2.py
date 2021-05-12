import requests as rq

class WeatherApi:

  def predict(self, hoursPredict):
    days=hoursPredict/24
    url = "http://api.weatherapi.com/v1/forecast.json?key=52f1b30e6fb84dbc886103154211205&q=San Francisco&days="+str(days)

    response = rq.get(url).json()
    prediction = response["forecast"]["forecastday"]
    forecasts = []

    for day in prediction:
      forecasts += day['hour']

    forecast_hourly = []

    for item in forecasts:
      forecast_hourly.append({'temp': item['temp_c'], 'hum': item['humidity'], 'hour': item['time']})


    return {
      'periods': hoursPredict,
      'prediction': forecast_hourly
    }