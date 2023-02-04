import sys

import pygame

import game
from assets import asset_loader
from assets.asset_loader import CLICK_SOUND


class MainMenu:
    def __init__(self):
        self.__rects = []
        self.__loaded = False

    def button_tick(self):
        mouse = pygame.mouse
        for name, rect in self.__rects:
            if rect.collidepoint(
                    mouse.get_pos()):
                CLICK_SOUND.play()
                if name == 'song browser':
                    game.GameWindow.game_state = game.GameStates.LEVEL_BROWSER
                elif name == "settings":
                    game.GameWindow.game_state = game.GameStates.SETTINGS
                elif name == "tutorial":
                    game.GameWindow.game_state = game.GameStates.TUTORIAL
                elif name == "quit":
                    game.GameWindow.database.save()
                    pygame.quit()
                    sys.exit(1)

    def render(self, surface: pygame.Surface):
        bg = pygame.Surface((1440, 800))
        bg.fill((255, 255, 255))
        game.GameWindow.game_background.blit(bg, (0, 0))

        # Variables
        main_title = asset_loader.main_font.render("Jukebox Mania", True, (0, 0, 0))
        copyright_text = asset_loader.small_font.render('A Game By Ido Geva', True, (0, 0, 0))

        # Buttons
        song_browser = asset_loader.medium_font.render("Song Browser", True, (0, 0, 0))
        tutorial = asset_loader.medium_font.render("Tutorial", True, (0, 0, 0))
        settings = asset_loader.medium_font.render("Settings", True, (0, 0, 0))
        quit_button = asset_loader.medium_font.render("Quit Game", True, (0, 0, 0))

        self.__rects.append(("song browser", song_browser.get_rect(center=(game.GameConstants.CENTER[0], 200))))
        self.__rects.append(("tutorial", tutorial.get_rect(center=(game.GameConstants.CENTER[0], 300))))
        self.__rects.append(("settings", settings.get_rect(center=(game.GameConstants.CENTER[0], 400))))
        self.__rects.append(("quit", quit_button.get_rect(center=(game.GameConstants.CENTER[0], 500))))

        # Blits
        surface.blit(main_title, main_title.get_rect(center=(game.GameConstants.CENTER[0], 50)))
        surface.blit(copyright_text, copyright_text.get_rect(center=(120, 780)))
        surface.blit(song_browser, song_browser.get_rect(center=(game.GameConstants.CENTER[0], 200)))
        surface.blit(tutorial, tutorial.get_rect(center=(game.GameConstants.CENTER[0], 300)))
        surface.blit(settings, settings.get_rect(center=(game.GameConstants.CENTER[0], 400)))
        surface.blit(quit_button, quit_button.get_rect(center=(game.GameConstants.CENTER[0], 500)))

        return self
