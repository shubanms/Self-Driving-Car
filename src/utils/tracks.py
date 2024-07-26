import pygame

import numpy as np

from src.utils import constants


def expand_path(points: list, thickness: int):
    """
    Expand the given points into an outer and inner path.

    Args:
        points (list): List of points representing the track.
        thickness (int): The thickness of the track.

    Returns:
        tuple: Two lists of points representing the inner and outer paths.
    """

    def get_perpendicular_vector(p1, p2, offset):
        """Calculate the perpendicular vector with a given offset."""

        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        length = np.sqrt(dx**2 + dy**2)
        if length == 0:
            return (0, 0)
        perp_x = -dy / length * offset
        perp_y = dx / length * offset
        return (perp_x, perp_y)

    outer_points = []
    inner_points = []

    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        perpendicular_vector = get_perpendicular_vector(p1, p2, thickness / 2)

        outer_points.append(
            (p1[0] + perpendicular_vector[0], p1[1] + perpendicular_vector[1]))
        inner_points.append(
            (p1[0] - perpendicular_vector[0], p1[1] - perpendicular_vector[1]))

    outer_points.append(
        (points[-1][0] + perpendicular_vector[0], points[-1][1] + perpendicular_vector[1]))
    inner_points.append(
        (points[-1][0] - perpendicular_vector[0], points[-1][1] - perpendicular_vector[1]))

    return inner_points, outer_points


def draw_paths(screen, inner_points, outer_points):
    """
    Draw the inner and outer paths on the Pygame screen.

    Args:
        screen (pygame.Surface): The pygame surface to draw on.
        inner_points (list): List of tuples representing the inner path.
        outer_points (list): List of tuples representing the outer path.
    """

    if inner_points and outer_points:
        pygame.draw.lines(screen, constants.WHITE_COLOR,
                          False, inner_points, 2)
        pygame.draw.lines(screen, constants.WHITE_COLOR,
                          False, outer_points, 2)