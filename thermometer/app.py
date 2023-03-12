from flask import Flask
from thermometer import Thermometer

app = Flask('Thermometer App')


@app.route('/')
def get_hello():
    t1 = Thermometer(0, 10)
    return "Hello World " + str(t1.boiling_threshold)