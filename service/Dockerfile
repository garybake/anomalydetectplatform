FROM python:3.7-slim

RUN mkdir src
WORKDIR /src

COPY requirements.txt main.py model.joblib ./
RUN pip install -r requirements.txt

CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000
