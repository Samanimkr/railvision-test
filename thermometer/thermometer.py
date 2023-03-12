import random
from utils.repeated_timer import RepeatedTimer
from sqlalchemy.orm import sessionmaker
import db

Session = sessionmaker(db.db_engine)
session = Session()


class Thermometer:
    current_temp = 5

    def __init__(self, freezing, boiling):
        self.freezing_threshold = freezing
        self.boiling_threshold = boiling

        thermometer = db.Thermometer()
        session.add(thermometer)
        session.commit()

        self.id = thermometer.id
        self.temp_timer = RepeatedTimer(1, self.read_temperature)

    def read_temperature(self):
        self.current_temp = self.current_temp + random.choice([-0.5, 0, 0.5])
        temperature = db.Temperature(thermometer_id=self.id, temperature=self.current_temp)

        session.add(temperature)
        session.commit()
        print(temperature.temperature)

    def notify_user(self):
        pass
