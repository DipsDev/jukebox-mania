import pygame

import game


class MainMenu:
    def __init__(self):
        pass

    def render(self, surface: pygame.Surface):
        # Variables
        main_title = game.main_font.render("Jukebox Mania", True, (0, 0, 0))
        copyright = game.small_font.render('A Game By Ido Geva', True, (0, 0, 0))

        # Blits
        surface.blit(main_title, main_title.get_rect(center=(game.GameConstants.CENTER[0], 50)))
        surface.blit(copyright, copyright.get_rect(center=(100, 780)))
