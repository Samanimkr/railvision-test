# Railvision Thermometer App 
This application is a thermometer where you can set arbitrary thresholds, such as freezing and boiling,
and whether or not to receive notifications when the temperature crosses them.
The application follows a 3-tier architecture and leverages Docker Compose to run three containers:
- Database: runs a Postgres image on port `5432`
- API Server: python image running on port `3000`. (Depends on the Database service being healthy)
- Thermometer: python image running on port `3001`. (Depends on the Database service being healthy)


## How to run
1. In the terminal run this command:
```commandline
 docker compose up --build "thermometer" --build "server" --build "db" --attach server --attach thermometer
```

2. Then once everything is running use the `POST /create` endpoint on the server to create a thermometer

---
# Server

This is a Python Flask application that serves two endpoints: /create and /temperature_notification.

`POST /create` - receives JSON data, which it forwards to the Thermometer app to create the thermometer trigger the readings

`POST /temperature_notification` - receives JSON data containing a freezing/boiling notification of a specific thermometer, which it forwards to a webhook URL stored in `.env`.

---
# Thermometer
The `Thermometer` class simulates a thermometer that can read temperatures (currently randomly generated) and notify users when the temperature reaches certain thresholds.

### Creating a new thermometer
To create a new thermometer, send a POST request to the root endpoint (/) with a JSON payload containing the desired temperature thresholds and notification settings:

```json
{
   "freezing_threshold": 0.0,
    "boiling_threshold": 10.0,
    "ignore_notifs_within_range": 0.0,
    "notify_from_below_freezing": true,
    "notify_from_above_freezing": true,
    "notify_from_below_boiling": true,
    "notify_from_above_boiling": true
}
```
If the thermometer is created successfully, the endpoint will return a 200 status code and a message indicating that the thermometer was created successfully.

### Parameters
* `freezing_threshold`: The temperature at which the thermometer will notify the user its reached the 'FREEZING' point. Default value is 0.0.
* `boiling_threshold`: The temperature at which the thermometer will notify the user its reached the 'BOILING' point. Default value is 10.0.
* `ignore_notifs_within_range`: The range around the thresholds which any notifications will be ignored. Default value is 0.0.
* `notify_from_below_freezing`: Indicates whether to notify the user when the temperature reaches the freezing threshold from below. Default value is True.
* `notify_from_above_freezing`: Indicates whether to notify the user when the temperature reaches the freezing threshold from above. Default value is True.
* `notify_from_below_boiling`: Indicates whether to notify the user when the temperature reaches the boiling threshold from below. Default value is True.
* `notify_from_above_boiling`: Indicates whether to notify the user when the temperature reaches the boiling threshold from above. Default value is True.

### Methods
* `stop_reading()`: Stops the thermometer from reading/generating temperatures.
* `read_temperature()`: Generates a temperature and inserts it into the database. If the temperature reaches a certain threshold, the user will be notified.
* `notify_user()`: Sends a POST request to the server with the thermometer ID and the notification type (**BOILING** or **FREEZING**).

---
# Database
This application uses a PostgreSQL database that's accessed through SQLAlchemy. There's currently two models:

### Thermometer Model
The Thermometer model has the following attributes:

* `id`: uniquely generated UUID
* `created_at`: DateTime
* `freezing_threshold`: Float
* `boiling_threshold`: Float 
* `ignore_notifs_within_range`: Float
* `notify_from_below_freezing`: Boolean
* `notify_from_above_freezing`: Boolean
* `notify_from_below_boiling`: Boolean
* `notify_from_above_boiling`: Boolean
* The `Thermometer model` also has a relationship with the `Temperature model`, which is a one-to-many relationship

### Temperature Model
The Temperature model has the following attributes:

* `id`: uniquely generated UUID
* `created_at`: DateTime
* `temperature`: Float
* The `Temperature model` has a relationship with the `Thermometer model`, which is a many-to-one relationship.