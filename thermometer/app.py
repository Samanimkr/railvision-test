from flask import Flask, request
from thermometer import Thermometer

app = Flask(__name__)


@app.route('/', methods=['POST'])
def create_thermometer():
    data = request.get_json()

    Thermometer(
        freezing_threshold=data['freezing_threshold'],
        boiling_threshold=data['boiling_threshold'],
        ignore_notifs_within_range=data['ignore_notifs_within_range'],
        notify_from_below_freezing=data['notify_from_below_freezing'],
        notify_from_above_freezing=data['notify_from_above_freezing'],
        notify_from_below_boiling=data['notify_from_below_boiling'],
        notify_from_above_boiling=data['notify_from_above_boiling']
    )
    return 'Created thermometer successfully!', 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001, debug=True)
