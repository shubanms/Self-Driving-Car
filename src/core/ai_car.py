import math

from typing import List

from src.core.car import Car
from src.core.model import Model
from src.schemas.model_inputs import ModelInputs
from src.core.paths import Paths

paths = Paths()


class AIControlledCar(Car):
    def __init__(self, screen, x, y, dimensions, path, show_sensors, number_of_sensors, collisions):
        super().__init__(screen, x, y, dimensions, path,
                         show_sensors, number_of_sensors, collisions)

        self.model = Model()

    def get_sensors_distance(self, draw_sensor: bool) -> List[tuple]:
        if self.number_of_sensors == 3:
            directions = [0, 45, -45]
        elif self.number_of_sensors == 5:
            directions = [0, 45, -45, 90, -90]
        else:
            raise ValueError(f"Invalid number of sensors: {
                             self.number_of_sensors}")

        sensor_distance = list()

        for direction in directions:
            angle = self.angle + direction
            radians = math.radians(angle)
            cos_angle = math.cos(radians)
            sin_angle = math.sin(radians)

            hit_point = None
            max_distance = 100

            for distance in range(max_distance):
                x_end = self.x + distance * cos_angle
                y_end = self.y + distance * sin_angle

                if not paths.is_point_within_track(x_end, y_end, self.inner_points, self.outer_points):
                    hit_point = (x_end, y_end)
                    break

            if hit_point is None:
                x_end = self.x + max_distance * cos_angle
                y_end = self.y + max_distance * sin_angle
                hit_point = (x_end, y_end)

            if draw_sensor:
                super()._draw_sensors(hit_point)

            distance_to_obstacle = math.sqrt(
                (hit_point[0] - self.x) ** 2 + (hit_point[1] - self.y) ** 2)
            sensor_distance.append(distance_to_obstacle)

        return sensor_distance

    def move(self, keys=None):
        model_inputs = ModelInputs(
            speed=self.speed, sensors=self.get_sensors_distance(self.show_sensors), points=self.points)

        self.model.show_inputs(model_inputs)
