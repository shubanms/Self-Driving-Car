import pygame

import numpy as np
import matplotlib.pyplot as plt

from src.helper.tracks import expand_path

def main():
    pygame.init()
    screen = pygame.display.set_mode((1180, 620))
    pygame.display.set_caption("Draw Rough Track")
    clock = pygame.time.Clock()

    drawing = True
    points = []
    drawing_active = False

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
                if event.key == pygame.K_RETURN:
                    drawing = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        if len(points) > 1:
            pygame.draw.lines(screen, (255, 255, 255), False, points, 5)

        pygame.display.flip()

        clock.tick(60)

    inner_points, outer_points = expand_path(points, 30)
    
    inner_points_x = [i for i, j in inner_points]
    inner_points_x.extend([inner_points[0][0]])
    
    inner_points_y = [620 - j for i, j in inner_points]
    inner_points_y.extend([620 - inner_points[0][1]])
    
    outer_points_x = [i for i, j in outer_points]
    outer_points_x.extend([outer_points[0][0]])
    
    outer_points_y = [620 - j for i, j in outer_points]
    outer_points_y.extend([620 - outer_points[0][1]])
    
    inner_points_x, inner_points_y, outer_points_x, outer_points_y = np.array(inner_points_x), np.array(inner_points_y), np.array(outer_points_x), np.array(outer_points_y)
    
    plt.plot(inner_points_x, inner_points_y)
    plt.plot(outer_points_x, outer_points_y)
    
    plt.show()

    pygame.quit()


if __name__ == "__main__":
    main()
