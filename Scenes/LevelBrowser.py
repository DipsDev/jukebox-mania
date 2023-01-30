import pygame

import game
from Level import Level
from components import MusicTicket
from utils.LevelLoader import LevelLoader


class LevelBrowser:
    def __init__(self):
        self.__av_levels = LevelLoader().get_available_levels()
        game.GameWindow.level_running = None
        self.__loaded = False

    def load(self):
        if self.__loaded:
            return
        # Background importing --------------------------
        background_img = pygame.image.load("./assets/level_browser_bg.png").convert()
        background_img = pygame.transform.scale(background_img, game.GameConstants.DIMENSIONS)

        # Text and UI --------------------------
        level_browser = game.main_font.render("Song Browser", True, (255, 255, 255))
        background_img.blit(level_browser, level_browser.get_rect(center=(1440 / 2, 50)))

        # Blit to the screen --------------------------
        game.GameWindow.game_background.blit(background_img, (0, 0))
        game.GameWindow.combo_counter = 0

    def render(self, surface: pygame.Surface):

        pos = (game.GameConstants.DIMENSIONS[0] / 2, 100)
        for index, level_name in enumerate(self.__av_levels):
            MusicTicket.render(surface, level_name, pos, index)
