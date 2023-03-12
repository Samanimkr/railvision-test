from flask import Flask
app = Flask('Thermometer Server')


@app.route('/')
def get_hello():
    return "Hello World"
