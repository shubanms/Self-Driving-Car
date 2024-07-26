import sys
import pygame

from pprint import pprint
from src.utils import constants


class GameScreen:
    def __init__(self, screen):
        self.current_state = constants.DRAW_SCREEN
        self.clock = pygame.time.Clock()
        self.drawing_active = True
        self.screen = screen

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def show_drawing_screen(self):
        initial_track_points = list()
        self.screen.fill(constants.BLACK_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                pprint("Mouse down!")
                if not self.drawing_active:
                    mouse_position = pygame.mouse.get_pos()
                    initial_track_points.append(mouse_position)

                    self.drawing_active = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.drawing_active = False

            if event.type == pygame.MOUSEMOTION:
                if self.drawing_active:
                    mouse_position = pygame.mouse.get_pos()

                    if len(initial_track_points) == 0 or initial_track_points[-1] != mouse_position:
                        initial_track_points.append(mouse_position)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.drawing_active = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        if len(initial_track_points) > 1:
            pygame.draw.lines(self.current_screen, constants.WHITE_COLOR,
                              False, initial_track_points, constants.DRAWN_TRACK_SIZE)

        self.current_screen = constants.EDIT_SCREEN

        pygame.display.flip()
        
        self.clock.tick(constants.FPS)
        
        if self.current_screen != constants.DRAW_SCREEN:
            self.run()

    def show_edit_screen(self):
        print("NEW SCREEN!")
        pass

    def show_final_screen(self):
        pass

    def run(self):
        # while True:
        if self.current_state == constants.DRAW_SCREEN:
            pprint("Entering the Drawing Screen! !!")
            self.show_drawing_screen()
        elif self.current_screen == constants.EDIT_SCREEN:
            pprint("Entering the Editing Screen!")
            self.show_edit_screen()
        elif self.current_screen == constants.FINAL_SCREEN:
            pprint("Entering the Final Screen!")
            self.show_final_screen()

