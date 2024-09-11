from src.core.car import Car
from src.core.model import Model

class AIControlledCar(Car):
    def __init__(self, screen, x, y, dimensions, path, number_of_sensors, show_sensors, collisions, model):
        super().__init__(screen, x, y, dimensions, path, number_of_sensors, show_sensors, collisions)
        
        self.model = model

    def move(self, keys=None):
        self.calculate_sensor_distances()
        inputs = {
            "speed": self.speed,
            "sensor_distances": self.sensor_distances,
            "position": (self.x, self.y),
            "score": self.score
        }
