from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/prediction")
async def prediction():
    return {"message": "prediction World"}
