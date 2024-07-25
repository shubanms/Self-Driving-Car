import pygame

from pprint import pprint
from src.helper.tracks import expand_path, draw_paths
from src.utils import constants


def main():
    pygame.init()
    drawing_screen = pygame.display.set_mode(constants.SCREEN_DIMENSION)
    pygame.display.set_caption(constants.DRAWING_SCREEN_CAPTION)
    clock = pygame.time.Clock()

    drawing = True
    points = list()
    drawing_active = False

    while drawing:
        drawing_screen.fill(constants.BLACK_COLOR)

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
                if event.key == pygame.K_RETURN:
                    drawing = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        if len(points) > 1:
            pygame.draw.lines(drawing_screen, constants.WHITE_COLOR,
                              False, points, constants.DRAWN_TRACK_SIZE)

        pygame.display.flip()

        clock.tick(constants.FPS)

    inner_points, outer_points = expand_path(points, 40)

    pygame.init()
    final_screen = pygame.display.set_mode(constants.SCREEN_DIMENSION)
    pygame.display.set_caption(constants.FINAL_SCREEN_CAPTION)
    clock = pygame.time.Clock()

    running = True

    while running:
        final_screen.fill(constants.BLACK_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        draw_paths(final_screen, inner_points, outer_points)
        
        pygame.draw.circle(final_screen, constants.RED_COLOR, ((inner_points[0][0]+outer_points[0][0])/2, (inner_points[0][1]+outer_points[0][1])/2), 2)

        pygame.display.flip()

        clock.tick(constants.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
