import pygame

from src.core.tracks import Tracks
from src.utils import constants
from src.core.car import Car

tracks = Tracks()


def main():
    # Drawing Screen

    pygame.init()
    screen = pygame.display.set_mode(constants.SCREEN_DIMENSION)
    pygame.display.set_caption(constants.DRAWING_SCREEN_CAPTION)
    clock = pygame.time.Clock()

    drawing = True
    points = list()
    drawing_active = False

    while drawing:
        screen.fill(constants.BLACK_COLOR)

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
            pygame.draw.lines(screen, constants.WHITE_COLOR,
                              False, points, constants.DRAWN_TRACK_SIZE)

        pygame.display.flip()

        clock.tick(constants.FPS)

    inner_points, outer_points = tracks.expand_path(
        points, constants.FINAL_TRACK_SIZE)

    # Edit screen

    pygame.init()
    edit_screen = pygame.display.set_mode(constants.SCREEN_DIMENSION)
    pygame.display.set_caption(constants.FINAL_SCREEN_CAPTION)

    running = True
    erasing = False

    while running:
        edit_screen.fill(constants.BLACK_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    erasing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    erasing = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        if erasing:
            mouse_position = pygame.mouse.get_pos()
            pygame.draw.circle(screen, constants.WHITE_COLOR,
                               mouse_position, constants.ERASER_RADIUS)
            inner_points[:] = tracks.erase_points(
                inner_points, mouse_position, constants.ERASER_RADIUS)
            outer_points[:] = tracks.erase_points(
                outer_points, mouse_position, constants.ERASER_RADIUS)

        tracks.draw_paths(edit_screen, inner_points, outer_points)

        starting_point_x, starting_point_y = (
            (inner_points[0][0] + outer_points[0][0]) / 2, (inner_points[0][1] + outer_points[0][1]) / 2)

        pygame.display.flip()

        clock.tick(constants.FPS)

    # Final Screen

    pygame.init()
    final_screen = pygame.display.set_mode(constants.SCREEN_DIMENSION)
    pygame.display.set_caption(constants.EDITING_SCREEN_CAPTION)

    car_body = pygame.image.load(constants.CAR_BODY_FILE_PATH)
    car_body = pygame.transform.scale(car_body, constants.CAR_DIMENSIONS)

    car = Car(
        screen=final_screen,
        x=starting_point_x,
        y=starting_point_y,
        show_sensors=True,
        number_of_sensors=5,
        dimensions=constants.CAR_DIMENSIONS,
        path=(inner_points, outer_points),
        collisions=False
    )

    running = True

    while running:
        final_screen.fill(constants.BLACK_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        keys = pygame.key.get_pressed()
        car.move(keys)

        tracks.draw_paths(final_screen, inner_points, outer_points)

        car.draw(car_body)

        car.show_points()

        pygame.display.flip()
        clock.tick(constants.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
