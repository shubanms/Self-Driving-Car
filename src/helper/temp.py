import pygame
import numpy as np

def expand_path(points, thickness):
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
        perp_vector = get_perpendicular_vector(p1, p2, thickness / 2)
        
        outer_points.append((p1[0] + perp_vector[0], p1[1] + perp_vector[1]))
        inner_points.append((p1[0] - perp_vector[0], p1[1] - perp_vector[1]))

    outer_points.append((points[-1][0] + perp_vector[0], points[-1][1] + perp_vector[1]))
    inner_points.append((points[-1][0] - perp_vector[0], points[-1][1] - perp_vector[1]))
    
    return inner_points, outer_points

def draw_track(screen, inner_points, outer_points):
    """
    Draw the track with a green road between the inner and outer paths.

    Args:
        screen (pygame.Surface): The pygame surface to draw on.
        inner_points (list): List of points representing the inner path.
        outer_points (list): List of points representing the outer path.
    """
    # Draw the road (green) between inner and outer paths
    track_points = inner_points + list(reversed(outer_points))
    pygame.draw.polygon(screen, (0, 255, 0), track_points, 0)
    
    # Draw the outer and inner paths
    pygame.draw.polygon(screen, (255, 0, 0), outer_points, 0)  # Outer path boundary
    pygame.draw.polygon(screen, (0, 0, 0), inner_points, 0)    # Inner path boundary

def draw_thick_track(screen, points, thickness):
    """
    Draw a thick track by drawing lines connecting the points.

    Args:
        screen (pygame.Surface): The pygame surface to draw on.
        points (list): List of points representing the track.
        thickness (int): The thickness of the track.
    """
    if len(points) > 1:
        pygame.draw.lines(screen, (255, 255, 255), False, points, thickness)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1180, 620))
    pygame.display.set_caption("Draw Rough Track")
    clock = pygame.time.Clock()

    drawing = True
    points = []
    drawing_active = False
    thickness = 20  # Thickness of the track

    while drawing:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not drawing_active:
                    pos = pygame.mouse.get_pos()
                    points.append(pos)
                    drawing_active = True

            if event.type == pygame.MOUSEBUTTONUP:
                drawing_active = False

            if event.type == pygame.MOUSEMOTION:
                if drawing_active:
                    pos = pygame.mouse.get_pos()
                    if len(points) == 0 or points[-1] != pos:
                        points.append(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter key
                    drawing = False
                if event.key == pygame.K_ESCAPE:  # Escape key to quit
                    pygame.quit()
                    return

        if len(points) > 1:
            draw_thick_track(screen, points, thickness)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    
    # Calculate the outer and inner paths
    inner_points, outer_points = expand_path(points, thickness)

    # Create a new Pygame window for the final track
    pygame.init()
    final_screen = pygame.display.set_mode((1180, 620))
    pygame.display.set_caption("Final Track")
    final_clock = pygame.time.Clock()

    running = True
    while running:
        final_screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        draw_track(final_screen, inner_points, outer_points)

        pygame.display.flip()
        final_clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
