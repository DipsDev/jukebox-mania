import pygame

from utils.LevelLoader import LevelLoader


class LevelBrowser:
    def __init__(self):
        self.__av_levels = LevelLoader().get_available_levels()

    def render(self, surface: pygame.Surface):
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        level_browser = font.render("Level Browser", True, (0, 0, 0))
        surface.blit(level_browser, level_browser.get_rect(center=(1440/2, 50)))
        for index, level_name in enumerate(self.__av_levels):
            r = font.render(level_name, True, (0, 0, 0))
            surface.blit(r, r.get_rect(center=(1440 / 2, 50 + 100 * (index + 1))))
