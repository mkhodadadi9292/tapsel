from pydantic import BaseModel


class AdData(BaseModel):
    adId: int
    estimatedCVR: float
