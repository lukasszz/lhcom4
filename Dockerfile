FROM python:3.9-bullseye

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

