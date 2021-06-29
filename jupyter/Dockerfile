FROM python:3.7-slim

RUN mkdir src
WORKDIR /src

RUN pip install jupyter

CMD jupyter notebook --no-browser --allow-root --port 8080 --ip 0.0.0.0
