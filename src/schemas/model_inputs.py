from pydantic import BaseModel
from typing import List, Tuple


class ModelInputs(BaseModel):
    speed: float = 0.0
    sensors: List[float]
