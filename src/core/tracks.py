import pygame
import math

import numpy as np

from src.utils import constants


class Tracks:
    def __init__(self):
        pass

    def line_intersect(x1, y1, x2, y2, x3, y3, x4, y4) -> bool:
        """
            Helper function to determine if two line segments intersect.
        """
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

        return ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and \
            ccw((x1, y1), (x2, y2), (x3, y3)) != ccw(
                (x1, y1), (x2, y2), (x4, y4))

    def get_perpendicular_vector(self, p1, p2, offset) -> tuple:
        """
            Calculate the perpendicular vector with a given offset.
        """

        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        length = np.sqrt(dx**2 + dy**2)
        if length == 0:
            return (0, 0)
        perp_x = -dy / length * offset
        perp_y = dx / length * offset
        return (perp_x, perp_y)

    def expand_path(self, points: list, thickness: int) -> tuple:
        """
            Expand the given points into an outer and inner path.

            Args:
                points (list): List of points representing the track.
                thickness (int): The thickness of the track.

            Returns:
                tuple: Two lists of points representing the inner and outer paths.
        """
        outer_points = []
        inner_points = []

        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            perpendicular_vector = self.get_perpendicular_vector(
                p1, p2, thickness / 2)

            outer_points.append(
                (p1[0] + perpendicular_vector[0], p1[1] + perpendicular_vector[1]))
            inner_points.append(
                (p1[0] - perpendicular_vector[0], p1[1] - perpendicular_vector[1]))

        outer_points.append(
            (points[-1][0] + perpendicular_vector[0], points[-1][1] + perpendicular_vector[1]))
        inner_points.append(
            (points[-1][0] - perpendicular_vector[0], points[-1][1] - perpendicular_vector[1]))

        return inner_points, outer_points

    def draw_paths(self, screen: pygame.surface, inner_points: list, outer_points: list) -> None:
        """
            Draw the inner and outer paths on the Pygame screen.

            Args:
                screen (pygame.Surface): The pygame surface to draw on.
                inner_points (list): List of tuples representing the inner path.
                outer_points (list): List of tuples representing the outer path.

            Returns: None
        """

        if inner_points and outer_points:
            pygame.draw.lines(screen, constants.BLUE_COLOR,
                              False, inner_points, 2)
            pygame.draw.lines(screen, constants.BLUE_COLOR,
                              False, outer_points, 2)

    def erase_points(self, points: list, eraser_position: tuple, eraser_radius: int) -> list:
        """
            Erase points that are within the eraser radius from the given position.

            Args:
                points (list): A list of points of the line or track
                eraser_position (tuple): A tuple of the current eraser position (x, y)
                eraser_radius (int): The erasers radius

            Returns: (list) The list of points after the eraser has erased certain points from the track
        """
        return [p for p in points if math.dist(p, eraser_position) > eraser_radius]
