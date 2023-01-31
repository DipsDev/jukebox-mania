import pygame

import game


class MainMenu:
    def __init__(self):
        self.__rects = []

    def button_tick(self):
        mouse = pygame.mouse
        for name, rect in self.__rects:
            if rect.collidepoint(
                    mouse.get_pos()):
                if name == 'song browser':
                    game.GameWindow.game_state = game.GameStates.LEVEL_BROWSER

    def render(self, surface: pygame.Surface):
        # Variables
        main_title = game.main_font.render("Jukebox Mania", True, (0, 0, 0))
        copyright = game.small_font.render('A Game By Ido Geva', True, (0, 0, 0))

        # Buttons
        song_browser = game.medium_font.render("Song Browser", True, (0, 0, 0))
        tutorial = game.medium_font.render("Tutorial", True, (0, 0, 0))

        self.__rects.append(("song browser", song_browser.get_rect(center=(game.GameConstants.CENTER[0], 200))))
        self.__rects.append(("tutorial", tutorial.get_rect(center=(game.GameConstants.CENTER[0], 300))))

        # Blits
        surface.blit(main_title, main_title.get_rect(center=(game.GameConstants.CENTER[0], 50)))
        surface.blit(copyright, copyright.get_rect(center=(120, 780)))
        surface.blit(song_browser, song_browser.get_rect(center=(game.GameConstants.CENTER[0], 200)))
        surface.blit(tutorial, tutorial.get_rect(center=(game.GameConstants.CENTER[0], 300)))

        return self
