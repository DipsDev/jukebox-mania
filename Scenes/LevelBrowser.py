import pygame

from utils.LevelLoader import LevelLoader


class LevelBrowser:
    def __init__(self):
        self.__av_levels = LevelLoader().get_available_levels()

    def render(self, surface: pygame.Surface):
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        for index, level_name in enumerate(self.__av_levels):
            r = font.render(level_name, True, (0, 0, 0))
            surface.blit(r, dest=(100, 100 * index))
