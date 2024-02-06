from pydantic import BaseModel


class AdData(BaseModel):
    adId: int
    estimatedCVR: float


class StatModel(BaseModel):
    count: int
    avg_response_time: float
    p99_response_time: float
