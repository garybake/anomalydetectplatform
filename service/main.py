from typing import Optional, List

from fastapi import FastAPI
from joblib import load
from pydantic import BaseModel

MODEL_FILE ='model.joblib'

app = FastAPI()
app.ml_model = load(MODEL_FILE)

class Item(BaseModel):
    feature_vector: List[float]
    score: Optional[bool] = None


@app.get("/")
async def root():
    return {"message": "Welcome to prediction world!"}


@app.post("/prediction")
async def prediction(item: Item):
    pred = get_prediction(item.feature_vector)
    return {"is_inlier": str(pred)}


def get_prediction(feature_vector: List[float])-> bool :
    # TODO accept array of vectors
    pred = app.ml_model.predict([feature_vector])
    return pred[0] == 1