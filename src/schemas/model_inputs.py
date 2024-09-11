from pydantic import BaseModel
from typing import List


class ModelInputs(BaseModel):
    speed: float = 0.0
    sensors: List[float]
    points: float = 0.0
