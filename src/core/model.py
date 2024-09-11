import torch
import random
import os
import math

import numpy as np

from src.utils import constants
from src.schemas.model_inputs import ModelInputs


class Model:
    def __init__(self):
        print("Model initialized!")

    def show_inputs(self, model_input_data: ModelInputs):
        model_input_data = {
            "Car speed": model_input_data.speed,
            "Sensors distance": model_input_data.sensors,
            "Game score": model_input_data.points
        }

        print(model_input_data)
