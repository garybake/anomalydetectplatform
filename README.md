# Anomaly Detection Platform
Platform for anomaly detection and monitoring  

![Alt text](docs/AnomalyDetectionDashboard.png?raw=true "dashboard")

### Start Jupyter

    make jupyter_build
    make jupyter_run


### Start Web Service

    make service_run
    make service_run_local

http://127.0.0.1:8000/docs

Predict vector

    curl -X 'POST' \
        'http://localhost:8000/prediction' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "feature_vector": [
            1.2, 3.4
        ],
        "score": false
    }'

Predict vector with scoring

    curl -X 'POST' \
        'http://localhost:8000/prediction' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "feature_vector": [
            31.2, 32.4
        ],
        "score": true
    }'

Get model parameters

    curl -X 'GET' \
        'http://localhost:8000/model_information' \
        -H 'accept: application/json'

### Monitoring Service


    cd monitoring
    docker-compose up -d


Prometheus - Monitoring system  
http://127.0.0.1:9090/graph

Grafana - Analytics dashboard  
http://127.0.0.1:3000/login

Caddy - Reverse proxy for basic auth  