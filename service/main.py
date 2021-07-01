from typing import Optional, List

from fastapi import FastAPI, HTTPException
from joblib import load
from pydantic import BaseModel

MODEL_FILE ='model.joblib'

app = FastAPI(    
    title="Anomaly Detection Platform",
    description="This is a very fancy project to detect anomalies",
    version="0.0.1",
)
app.ml_model = load(MODEL_FILE)

class PredictIn(BaseModel):
    feature_vector: List[float]
    score: Optional[bool] = False

class PredictOut(BaseModel):
    is_inlier: bool
    anomaly_score: Optional[float] = None


@app.get("/")
async def root():
    return {"message": "Welcome to prediction world!"}


@app.post("/prediction", response_model=PredictOut)
async def post_prediction(pred_in: PredictIn):
    if len(pred_in.feature_vector) != 2:
        raise HTTPException(status_code=404, detail="Invalid feature vector, should be [float, float]")

    pred = get_prediction(pred_in.feature_vector)
    ret = {"is_inlier": pred}

    if pred_in.score:
        score = get_score(pred_in.feature_vector)
        ret['anomaly_score'] = score

    return ret

@app.get('/model_information')
async def get_model_information():
    return app.ml_model.get_params()


def get_prediction(feature_vector: List[float]) -> bool :
    # TODO accept array of vectors
    pred = app.ml_model.predict([feature_vector])
    return pred[0] == 1

def get_score(feature_vector: List[float]) -> float :
    scores = app.ml_model.score_samples([feature_vector])
    return scores[0]
