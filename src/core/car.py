import pygame
import sys
import math

from src.utils import constants


class Car:
    def __init__(self, x: float, y: float):
        """
            Creates the Car object on the game screen.

            Args:
                x (float): Takes the X co-ord of the starting point of the car
                y (float): Takes the Y co-ord of the starting point of the car

        """

        # Set initial position and metrics of the car
        self.x = x
        self.y = y
        self.angle = constants.CAR_ANGLE
        self.speed = constants.CAR_INITIAL_SPEED
        self.size = constants.CAR_SIZE

        # Set movement metrics for the car
        self.top_speed = constants.CAR_TOP_SPEED
        self.acceleration = constants.CAR_ACCELERATION
        self.deceleration = constants.CAR_DECELERATION
        self.turning_radius = constants.CAR_TURNING_RADIUS

    def draw(self, screen, car_body):
        rotated_car = pygame.transform.rotate(car_body, -self.angle)
        new_rect = rotated_car.get_rect(center=(self.x, self.y))
        screen.blit(rotated_car, new_rect.topleft)

    def move(self, key):
        """
            Moves around the Car object on the game screen with key presses

            Args:
                key: Any pygame key press ['W', 'A', 'S', 'D'] to move the car in all four directions.
        """

        # ! Implement it such that even arrow keys work

        # Check if the car has gained any velocity or acceleration
        if key[pygame.K_w]:
            self.speed = min(self.speed + self.acceleration, self.top_speed)
        elif key[pygame.K_s]:
            self.speed = max(self.speed - self.acceleration, -self.top_speed)
        else:
            if self.speed > 0:
                self.speed = max(self.speed - self.deceleration, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + self.deceleration, 0)

        # Check if the car has rotated in any direction
        if key[pygame.K_a]:
            self.angle -= self.turning_radius
        elif key[pygame.K_d]:
            self.angle += self.turning_radius

        # Update the position of the car using the speed and the angle it has rotated
        radians = math.radians(self.angle)
        self.x += self.speed * math.cos(radians)
        self.y += self.speed * math.sin(radians)

        # Check if the car touches or crashed with the outer game window boundary
        # if self.x < constants.SCREEN_WIDTH or self.x > 0 or self.y < constants.SCREEN_HEIGHT or self.y > 0:
        #     print("Crashed!")
        #     pygame.quit()
        #     sys.exit()
