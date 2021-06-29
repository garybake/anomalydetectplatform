FROM python:3.7-slim

RUN mkdir src
WORKDIR /src

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD jupyter notebook --no-browser --allow-root --port 8080 --ip 0.0.0.0
