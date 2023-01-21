import pygame

import game
from Level import Level
from utils.LevelLoader import LevelLoader


class LevelBrowser:
    def __init__(self):
        self.__av_levels = LevelLoader().get_available_levels()
        game.GameWindow.level_running = None

    def render(self, surface: pygame.Surface):

        level_browser = game.main_font.render("Level Browser", True, (0, 0, 0))
        surface.blit(level_browser, level_browser.get_rect(center=(1440/2, 50)))
        mouse = pygame.mouse
        for index, level_name in enumerate(self.__av_levels):
            r = game.main_font.render(level_name, True, (0, 0, 0))
            surface.blit(r, r.get_rect(center=(1440 / 2, 50 + 100 * (index + 1))))
            if mouse.get_pressed()[0] and r.get_rect(center=(1440 / 2, 50 + 100 * (index + 1))).collidepoint(mouse.get_pos()):
                level_data = LevelLoader().load_level_beatmap(level_name.replace(" ", "_"))
                level = Level(level_data, game.keyboard_keys)
                game.GameWindow.level_running = level
                game.GameWindow.game_state = game.GameStates.PLAYING_LEVEL

