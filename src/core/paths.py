import pygame
import math


class Paths:
    def __init__(self):
        pass

    def line_intersect(self, x1, y1, x2, y2, x3, y3, x4, y4):
        """
        Helper function to determine if two line segments intersect.
        """
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

        return ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and \
            ccw((x1, y1), (x2, y2), (x3, y3)) != ccw(
                (x1, y1), (x2, y2), (x4, y4))

    def point_in_polygon(self, point, polygon):
        """
            Helper function to check if a point co-ordinate lies inside a given polygon

            Args:
                point (tuple): (x,y) co-ordinates
                polygon (list): The list of points that make up the polygon

            Returns:
                Bool: True of False, if the point lies within the given polygon
        """
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

    def is_point_within_track(self, x, y, inner_points, outer_points):
        """Check if a point is within the track boundaries."""

        return self.point_in_polygon((x, y), inner_points) and not self.point_in_polygon((x, y), outer_points)
