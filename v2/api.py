from flask import Flask
from predictV2 import WeatherApi

app = Flask(__name__)

predictor = WeatherApi()


@app.route('/servicio/v2/prediccion/24horas/')
def predict24():
    return predictor.predict(24), 200

@app.route('/servicio/v2/prediccion/48horas/')
def predict48():
    return predictor.predict(48), 200

@app.route('/servicio/v2/prediccion/72horas/')
def predict72():
    return predictor.predict(72), 200
