FROM python:3.8-slim-buster

ENV FLASK_APP=../thermometer/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=3001
ENV FLASK_ENV=development

WORKDIR ../thermometer

COPY ../requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ../thermometer .

CMD [ "python3", "-m" , "flask", "run"]