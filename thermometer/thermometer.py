import os
import random
from utils.repeated_timer import RepeatedTimer
from sqlalchemy.orm import sessionmaker
import db
import requests

Session = sessionmaker(db.db_engine)
session = Session()


class Thermometer:
    current_temp = 5
    left_freezing_ignore_range = True
    left_boiling_ignore_range = True

    def __init__(
            self,
            freezing_threshold=0.0,
            boiling_threshold=10.0,
            ignore_notifs_within_range=0.0,
            notify_from_below_freezing=True,
            notify_from_above_freezing=True,
            notify_from_below_boiling=True,
            notify_from_above_boiling=True
    ):
        self.freezing_threshold = freezing_threshold
        self.boiling_threshold = boiling_threshold
        self.ignore_notifs_within_range = ignore_notifs_within_range
        self.notify_from_below_freezing = notify_from_below_freezing
        self.notify_from_above_freezing = notify_from_above_freezing
        self.notify_from_below_boiling = notify_from_below_boiling
        self.notify_from_above_boiling = notify_from_above_boiling

        # Create thermometer record in DB
        thermometer = db.Thermometer(
            freezing_threshold=freezing_threshold,
            boiling_threshold=boiling_threshold,
            ignore_notifs_within_range=ignore_notifs_within_range,
            notify_from_below_freezing=notify_from_below_freezing,
            notify_from_above_freezing=notify_from_above_freezing,
            notify_from_below_boiling=notify_from_below_boiling,
            notify_from_above_boiling=notify_from_above_boiling,
        )
        session.add(thermometer)
        session.commit()

        self.id = thermometer.id
        self.read_temperature_timer = RepeatedTimer(1, self.read_temperature)

    def stop_reading(self):
        self.read_temperature_timer.stop()

    def read_temperature(self):
        # Randomly generate a temperature
        self.current_temp = min(15, max(-5, self.current_temp + random.choice([-0.5, 0, 0.5])))

        # Get last temperature reading
        last_reading_record = session \
            .query(db.Temperature) \
            .order_by(db.Temperature.created_at.desc()) \
            .where(db.Temperature.thermometer_id == self.id) \
            .first()
        last_reading = last_reading_record.temperature if last_reading_record else self.current_temp

        # Insert new temperature in DB
        temperature = db.Temperature(thermometer_id=self.id, temperature=self.current_temp)
        session.add(temperature)
        session.commit()

        # Notify user check
        if (not self.left_freezing_ignore_range and
                abs(self.current_temp - self.freezing_threshold) >= self.ignore_notifs_within_range):
            self.left_freezing_ignore_range = True
        if (not self.left_boiling_ignore_range and
                abs(self.current_temp - self.boiling_threshold) >= self.ignore_notifs_within_range):
            self.left_boiling_ignore_range = True

        should_notify_freezing = (
                self.left_freezing_ignore_range and
                self.current_temp == self.freezing_threshold and
                (last_reading > self.freezing_threshold and self.notify_from_above_freezing
                 or last_reading < self.freezing_threshold and self.notify_from_below_freezing)
        )
        should_notify_boiling = (
                self.left_boiling_ignore_range and
                self.current_temp == self.boiling_threshold and
                (last_reading > self.boiling_threshold and self.notify_from_above_boiling
                 or last_reading < self.boiling_threshold and self.notify_from_below_boiling)
        )

        if should_notify_freezing:
            self.left_freezing_ignore_range = False
            self.notify_user()
        elif should_notify_boiling:
            self.left_boiling_ignore_range = False
            self.notify_user()

        print(str(self.id) + ": " + str(temperature.temperature))

    def notify_user(self):
        notify_server_url = os.getenv('SERVER_URL') + '/temperature_notification'
        notification_type = "BOILING" if self.current_temp == self.boiling_threshold else "FREEZING"
        data = {
            'thermometer_id': str(self.id),
            'notification_type': notification_type
        }
        requests.post(url=notify_server_url, json=data)
