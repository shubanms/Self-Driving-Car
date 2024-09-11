import torch
import random
import os
import math

import numpy as np

from src.utils import constants
from src.schemas.model_inputs import ModelInputs


class Model:
    def __init__(self, inputs: ModelInputs):
        self.car_speed = inputs.speed
        self.number_of_sensors = len(inputs.sensors)
        self.sensor_distances: list = inputs.sensors
        self.points = inputs.points

    def show_inputs(self):
        model_input_data = {
            "Car speed": self.car_speed,
            "Number of sensors": self.number_of_sensors,
            "Sensors distance": self.sensor_distances,
            "Game score": self.points
        }

        print(model_input_data)
