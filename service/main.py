from typing import Optional, List
from time import perf_counter

from fastapi import FastAPI, HTTPException
from joblib import load
from pydantic import BaseModel

from prometheus_client import make_asgi_app, Counter, Histogram, Gauge

MODEL_FILE ='model.joblib'

app = FastAPI(    
    title="Anomaly Detection Platform",
    description="This is a very fancy project to detect anomalies",
    version="0.0.1",
)
app.ml_model = load(MODEL_FILE)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
c_prediction = Counter('c_prediction', 'prediction_endpoint')
c_model_information = Counter('c_model_information', 'model_information_endpoint')
h_prediction_output = Histogram('h_prediction_output', 'prediction_response_output_histogram')
h_prediction_score = Histogram('h_prediction_score', 'prediction_response_score_histogram')
h_prediction_latency = Histogram('h_prediction_latency', 'response_time_prediction_endpoint')
g_prediction_output = Gauge('g_prediction_output', 'prediction_output_guage')

class PredictIn(BaseModel):
    feature_vector: List[float]
    score: Optional[bool] = False

class PredictOut(BaseModel):
    is_inlier: bool
    anomaly_score: Optional[float] = None


@app.get("/")
async def root():
    return {"message": "Welcome to prediction world!"}


@h_prediction_latency.time()
@app.post("/prediction", response_model=PredictOut)
async def post_prediction(pred_in: PredictIn):
    c_prediction.inc()
    t_start = perf_counter() 
    if len(pred_in.feature_vector) != 2:
        raise HTTPException(status_code=404, detail="Invalid feature vector, should be [float, float]")

    pred = get_prediction(pred_in.feature_vector)
    ret = {"is_inlier": pred}
    h_prediction_output.observe(pred) 
    if pred:
        g_prediction_output.inc()
    else:
        g_prediction_output.dec()

    if pred_in.score:
        score = get_score(pred_in.feature_vector)
        ret['anomaly_score'] = score
        h_prediction_score.observe(score)

    t_stop = perf_counter()
    return ret

@app.get('/model_information')
async def get_model_information():
    c_model_information.inc()
    return app.ml_model.get_params()


def get_prediction(feature_vector: List[float]) -> bool :
    # TODO accept array of vectors
    pred = app.ml_model.predict([feature_vector])
    return pred[0] == 1

def get_score(feature_vector: List[float]) -> float :
    scores = app.ml_model.score_samples([feature_vector])
    return scores[0]
