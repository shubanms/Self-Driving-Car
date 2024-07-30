import pygame
import sys
import math

from src.utils import constants
from src.core.paths import Paths

paths = Paths()


class Car:
    def __init__(
        self,
        screen,
        x: float,
        y: float,
        dimensions: tuple,
        path: tuple,
        show_sensors: bool,
        number_of_sensors: int,
        collisions: bool = True
    ) -> None:
        """
            Creates the Car object on the game screen.

            Args:
                x (float): Takes the X co-ord of the starting point of the car
                y (float): Takes the Y co-ord of the starting point of the car

            Returns: None

        """

        self.screen = screen
        self.collisions = collisions
        self.show_sensors = show_sensors
        self.number_of_sensors = number_of_sensors
        self.points = 0

        # Set initial position and metrics of the car
        self.x = x
        self.y = y
        self.angle = constants.CAR_ANGLE
        self.speed = constants.CAR_INITIAL_SPEED
        self.size = constants.CAR_SIZE
        self.car_length = dimensions[0]
        self.car_width = dimensions[1]
        self.car_points_factor = constants.CAR_POINTS_FACTOR

        # Set movement metrics for the car
        self.top_speed = constants.CAR_TOP_SPEED
        self.acceleration = constants.CAR_ACCELERATION
        self.deceleration = constants.CAR_DECELERATION
        self.turning_radius = constants.CAR_TURNING_RADIUS

        # Track path
        self.inner_points = path[0]
        self.outer_points = path[1]

    def show_game_points(self) -> None:
        """
            Displays the score/points of the current running game.
        """

        font = pygame.font.Font(None, 36)
        points_text = font.render(
            f"Points: {round(self.points * self.car_points_factor, 0)}", True, (255, 255, 255))
        self.screen.blit(points_text, (constants.SCREEN_WIDTH - 150, 10))

    def _draw_sensors(self) -> None:
        """
            Draw the sensor lines to visualize the car's perception of its surroundings.

            Has two types, one with 3 sensors and another one with 5 sensors.

            3 sensors: [0, 45, -45], in angle from the car front.
            5 sensors: [0, 45, -45, 90, -90] in angle from the car front.
        """

        if self.number_of_sensors == 3:
            directions = [0, 45, -45]
        elif self.number_of_sensors == 5:
            directions = [0, 45, -45, 90, -90]

        for direction in directions:
            angle = self.angle + direction
            radians = math.radians(angle)
            cos_angle = math.cos(radians)
            sin_angle = math.sin(radians)

            # Calculate end point of the sensor line
            hit_point = None
            max_distance = 100

            for distance in range(max_distance):
                x_end = self.x + distance * cos_angle
                y_end = self.y + distance * sin_angle

                if not paths.is_point_within_track(x_end, y_end, self.inner_points, self.outer_points):
                    hit_point = (x_end, y_end)
                    break

            # If no collision is detected, draw the full sensor length
            if hit_point is None:
                x_end = self.x + max_distance * cos_angle
                y_end = self.y + max_distance * sin_angle
                hit_point = (x_end, y_end)

            pygame.draw.line(self.screen, constants.GREEN_COLOR,
                             (self.x, self.y), hit_point, 2)
            pygame.draw.circle(self.screen, constants.RED_COLOR,
                               (int(hit_point[0]), int(hit_point[1])), 3)

    def draw(self, car_body: pygame.image) -> None:
        """
            Draws the car object on the screen.
        """

        rotated_car = pygame.transform.rotate(car_body, -self.angle)
        new_rect = rotated_car.get_rect(center=(self.x, self.y))
        self.screen.blit(rotated_car, new_rect.topleft)

    def detect_collision(self):
        """
        Check if the car collides with the inner or outer paths.

        Args:
            car_x (float): The x position of the car.
            car_y (float): The y position of the car.
            car_width (float): The width of the car.
            car_height (float): The height of the car.
            inner_points (list of tuples): Points defining the inner path.
            outer_points (list of tuples): Points defining the outer path.

        Returns:
            bool: True if the car collides with either path, False otherwise.
        """

        # Car vertices based on the center position and size
        half_width = self.car_width / 4
        half_length = self.car_length / 4

        # Define car's bounding box (as a rectangle)
        car_vertices = [
            (self.x - half_width, self.y - half_length),  # Top-left
            (self.x + half_width, self.y - half_length),  # Top-right
            (self.x + half_width, self.y + half_length),  # Bottom-right
            (self.x - half_width, self.y + half_length)   # Bottom-left
        ]

        # Check collision with the inner path
        for i in range(len(self.inner_points) - 1):
            x1, y1 = self.inner_points[i]
            x2, y2 = self.inner_points[i + 1]

            for j in range(4):
                cx1, cy1 = car_vertices[j]
                cx2, cy2 = car_vertices[(j + 1) % 4]

                if paths.line_intersect(x1, y1, x2, y2, cx1, cy1, cx2, cy2):
                    return True

        # Check collision with the outer path
        for i in range(len(self.outer_points) - 1):
            x1, y1 = self.outer_points[i]
            x2, y2 = self.outer_points[i + 1]

            for j in range(4):
                cx1, cy1 = car_vertices[j]
                cx2, cy2 = car_vertices[(j + 1) % 4]

                if paths.line_intersect(x1, y1, x2, y2, cx1, cy1, cx2, cy2):
                    return True

        return False

    def move(self, key) -> None:
        """
            Moves around the Car object on the game screen with key presses

            Args:
                key: Any pygame key press ['W', 'A', 'S', 'D'] or the arrow keys to move the car in all four directions.
        """

        # Check if the car has gained any velocity or acceleration
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.speed = min(self.speed + self.acceleration, self.top_speed)
            self.points += 1
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            self.speed = max(self.speed - self.acceleration, -self.top_speed)
            self.points -= 1
        else:
            if self.speed > 0:
                self.speed = max(self.speed - self.deceleration, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + self.deceleration, 0)

        # Check if the car has rotated in any direction
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.angle -= self.turning_radius
        elif key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.angle += self.turning_radius

        # Update the position of the car using the speed and the angle it has rotated
        radians = math.radians(self.angle)
        self.x += self.speed * math.cos(radians)
        self.y += self.speed * math.sin(radians)

        # Shows sensors from the car if it is enabled
        if self.show_sensors:
            self._draw_sensors()

        # Applies collision to the car if it is enabled
        if self.collisions:
            if self.detect_collision():
                self.speed = 0
                print("Crashed!")
                pygame.quit()
                sys.exit()
