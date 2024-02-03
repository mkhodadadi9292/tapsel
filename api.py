from fastapi import FastAPI
from typing import List

app = FastAPI()


@app.post("/predict", summary="Get all related CRVs.")
async def predict(advertise_ids: List[int]):
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
