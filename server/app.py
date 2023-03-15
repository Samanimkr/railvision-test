import os
from flask import Flask, request
import requests

app = Flask(__name__)
thermometer_app_url = os.getenv("THERMOMETER_APP_URL")
webhook_url = os.getenv('WEBHOOK_URL')


@app.route('/create', methods=['POST'])
def create_thermometer():
    data = request.get_json()
    response = requests.post(thermometer_app_url+'/', json=data)
    return response.text


@app.route('/temperature_notification', methods=['POST'])
def temperature_notification():
    data = request.get_json()
    requests.post(webhook_url, json=data)

    return {'success': True}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
