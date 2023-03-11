from flask import Flask
app = Flask('Thermometer Server')


@app.route('/')
def get_hello():
    return "Hello World"


class Thermometer:
    currentTemp = 23

    def __init__(self, freezing, boiling):
        self.freezing_threshold = freezing
        self.boiling_threshold = boiling

    def __str__(self):
        return str(self.currentTemp)


t1 = Thermometer(0, 100)
print(t1)
