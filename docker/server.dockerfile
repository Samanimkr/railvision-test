FROM python:3.8-slim-buster

ENV FLASK_APP=../server/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

WORKDIR ../server

COPY ../requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ../server .

CMD [ "python3", "-m" , "flask", "run"]