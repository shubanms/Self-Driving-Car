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

    def show_inputs(self):
        print(self.car_speed)
        print(self.number_of_sensors)
        print(self.sensor_distances)
