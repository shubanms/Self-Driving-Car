import pygame
import sys
import math

from src.utils import constants


# TODO - Add all track like functionality in tracks
class Car:
    def __init__(self, screen, x: float, y: float, dimensions: tuple, path: tuple, show_sensors: bool, collisions: bool = True):
        """
            Creates the Car object on the game screen.

            Args:
                x (float): Takes the X co-ord of the starting point of the car
                y (float): Takes the Y co-ord of the starting point of the car

        """

        self.screen = screen
        self.collisions = collisions
        self.show_sensors = show_sensors

        # Set initial position and metrics of the car
        self.x = x
        self.y = y
        self.angle = constants.CAR_ANGLE
        self.speed = constants.CAR_INITIAL_SPEED
        self.size = constants.CAR_SIZE
        self.car_length = dimensions[0]
        self.car_width = dimensions[1]

        # Set movement metrics for the car
        self.top_speed = constants.CAR_TOP_SPEED
        self.acceleration = constants.CAR_ACCELERATION
        self.deceleration = constants.CAR_DECELERATION
        self.turning_radius = constants.CAR_TURNING_RADIUS

        # Track path
        self.inner_points = path[0]
        self.outer_points = path[1]

    def _line_intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        Helper function to determine if two line segments intersect.
        """
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

        return ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and \
            ccw((x1, y1), (x2, y2), (x3, y3)) != ccw(
                (x1, y1), (x2, y2), (x4, y4))

    def _is_point_within_track(self, x, y, inner_points, outer_points):
        """Check if a point is within the track boundaries."""
        def point_in_polygon(point, polygon):
            x, y = point
            n = len(polygon)
            inside = False

            p1x, p1y = polygon[0]
            for i in range(n + 1):
                p2x, p2y = polygon[i % n]
                if y > min(p1y, p2y):
                    if y <= max(p1y, p2y):
                        if x <= max(p1x, p2x):
                            if p1y != p2y:
                                xinters = (y - p1y) * (p2x - p1x) / \
                                    (p2y - p1y) + p1x
                            if p1x == p2x or x <= xinters:
                                inside = not inside
                p1x, p1y = p2x, p2y

            return inside

        return point_in_polygon((x, y), inner_points) and not point_in_polygon((x, y), outer_points)

    def _draw_sensors(self):
        """Draw the sensor lines to visualize the car's perception of its surroundings."""
        directions = [
            0, 45, -45]  # Straight, left-diagonal, right-diagonal, left-right sensors

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

                if not self._is_point_within_track(x_end, y_end, self.inner_points, self.outer_points):
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

    def draw(self, car_body):
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

                if self._line_intersect(x1, y1, x2, y2, cx1, cy1, cx2, cy2):
                    return True

        # Check collision with the outer path
        for i in range(len(self.outer_points) - 1):
            x1, y1 = self.outer_points[i]
            x2, y2 = self.outer_points[i + 1]

            for j in range(4):
                cx1, cy1 = car_vertices[j]
                cx2, cy2 = car_vertices[(j + 1) % 4]

                if self._line_intersect(x1, y1, x2, y2, cx1, cy1, cx2, cy2):
                    return True

        return False

    def move(self, key):
        """
            Moves around the Car object on the game screen with key presses

            Args:
                key: Any pygame key press ['W', 'A', 'S', 'D'] or the arrow keys to move the car in all four directions.
        """

        # TODO - Add in arrow keys as well for car control

        # Check if the car has gained any velocity or acceleration
        if key[pygame.K_w] or key[pygame.K_UP]:
            self.speed = min(self.speed + self.acceleration, self.top_speed)
        elif key[pygame.K_s] or key[pygame.K_DOWN]:
            self.speed = max(self.speed - self.acceleration, -self.top_speed)
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

        if self.show_sensors:
            self._draw_sensors()

        if self.collisions:
            if self.detect_collision():
                self.speed = 0
                print("Crashed!")
                pygame.quit()
                sys.exit()
